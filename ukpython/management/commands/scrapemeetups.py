from datetime import datetime
import re

import requests
from urllib.parse import ParseResult, urlencode, urlparse, urlunparse

from django.conf import settings
from django.core.management import BaseCommand, CommandError, call_command

from ...models import Event, UserGroup


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        call_command('loadpages')

        for group in UserGroup.objects.all():
            parsed_url = urlparse(group.url)
            if parsed_url.netloc != 'www.meetup.com':
                continue

            if kwargs['verbosity'] > 0:
                self.stdout.write('Retrieving meetups for {}'.format(group.name))

            # Capture everything except leading slash and optional trailing slash
            match = re.match('^/([^/]*)/?$', parsed_url.path)

            if not match:
                raise CommandError('URL not of form http://meetup.com/[identifier] for {}'.format(group.name))

            identifier = match.group(1)
            path = '/{}/events'.format(identifier)

            querystring = urlencode({
                'key': settings.MEETUP_API_KEY,
                'page': 100,
            })

            api_url = urlunparse(ParseResult(
                scheme='https',
                netloc='api.meetup.com',
                path=path,
                params='',
                query=querystring,
                fragment='',
            ))

            rsp = requests.get(api_url)
            rsp.raise_for_status()

            event_records = rsp.json()

            # Just in case 100 isn't enough!
            assert len(event_records) < 100, '100 results returned from Meetup API'

            for record in event_records:
                dt = datetime.fromtimestamp((record['time'] + record['utc_offset']) / 1000)

                if 'venue' in record:
                    venue_fields = []
                    for fieldname in ['name', 'address_1', 'address_2', 'city']:
                        if fieldname in record['venue']:
                            venue_fields.append(record['venue'][fieldname].strip())
                    venue = ', '.join(venue_fields)
                else:
                    venue = None

                event, created = Event.objects.update_or_create(
                    url=record['link'],
                    defaults={
                        'user_group': group,
                        'name': record['name'],
                        'date': dt.date(),
                        'time': dt.time(),
                        'venue': venue,
                    }
                )

                if kwargs['verbosity'] > 0 and created:
                    self.stdout.write('Added new event ({})'.format(record['name']))

        call_command('dumppages')
