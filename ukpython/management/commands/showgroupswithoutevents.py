import calendar

from django.core.management import BaseCommand

from ...models import UserGroup


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('year', type=int)
        parser.add_argument('month', type=int)

    def handle(self, *args, **kwargs):
        year = kwargs['year']
        month = kwargs['month']
        month_name = calendar.month_name[month]

        groups_with_no_events_scheduled = UserGroup.objects.no_events_scheduled(year, month)

        if groups_with_no_events_scheduled:
            print('The following groups have no events scheduled for {} {}'.format(month_name, year))
            for group in groups_with_no_events_scheduled:
                print(' * {}'.format(group.name))

        else:
            print('All groups have something scheduled for {} {}'.format(month_name, year))
