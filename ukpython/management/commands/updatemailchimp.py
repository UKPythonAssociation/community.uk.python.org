import calendar
from datetime import date

from django.core.management import BaseCommand, call_command

from ...mailchimp import update_mailchimp


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('year', type=int)
        parser.add_argument('month', type=int)

    def handle(self, *args, **kwargs):
        call_command('loadpages')
        update_mailchimp(kwargs['year'], kwargs['month'])
