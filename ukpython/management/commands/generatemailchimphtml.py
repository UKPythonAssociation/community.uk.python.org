import calendar
from datetime import date

from django.core.management import BaseCommand, call_command
from django.template.loader import get_template

from ...models import Event, NewsItem, UserGroup


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('year', type=int)
        parser.add_argument('month', type=int)

    def handle(self, *args, **kwargs):
        call_command('loadpages')

        year = kwargs['year']
        month = kwargs['month']

        news_items = NewsItem.objects.for_newsletter(year, month)

        upcoming_events = Event.objects.scheduled_in_month(year, month).order_by('date')
        groups_with_no_events_scheduled = UserGroup.objects.no_events_scheduled(year, month).order_by('name')

        month_name = calendar.month_name[month]
        next_month_name = calendar.month_name[(month + 1) % 12]
        next_month_deadline = date(year, month, 24)
        
        template = get_template('mailchimp-newsletter.html')

        context = {
            'news_items': news_items,
            'upcoming_events': upcoming_events,
            'groups_with_no_events_scheduled': groups_with_no_events_scheduled,
            'month_name': month_name,
            'next_month_name': next_month_name,
            'next_month_deadline': next_month_deadline,
        }

        self.stdout.write(template.render(context))
