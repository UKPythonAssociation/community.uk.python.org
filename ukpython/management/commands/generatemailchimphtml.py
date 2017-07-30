from datetime import date

from django.core.management import BaseCommand, call_command

from ...mailchimp import generate_html


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('year', type=int)
        parser.add_argument('month', type=int)

    def handle(self, *args, year, month, **kwargs):
        call_command('loadpages')
        print(generate_html(year, month))
