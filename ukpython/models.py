import datetime

from django.db import models
from django_amber.models import ModelWithoutContent, PagesManager


class UserGroup(ModelWithoutContent):
    name = models.CharField(max_length=255)
    url = models.URLField(null=True)

    dump_dir_path = 'user-groups'

    def __str__(self):
        return self.name

    class Manager(PagesManager):
        def no_events_scheduled(self, year, month):
            subquery = self.filter(event__date__year=year, event__date__month=month)
            return self.exclude(id__in=subquery)

    objects = Manager()

    def future_events(self):
        today = datetime.date.today()
        return self.events.filter(date__gte=today).order_by('date', 'time')

    def past_events(self):
        today = datetime.date.today()
        return self.events.filter(date__lt=today).order_by('date', 'time')

    def next_event(self):
        upcoming_events = self.future_events()
        if upcoming_events:
            return upcoming_events[0]
        else:
            return None

    def other_future_events(self):
        return self.future_events()[1:]


class Event(ModelWithoutContent):
    user_group = models.ForeignKey(UserGroup, related_name='events')
    name = models.CharField(max_length=255)
    url = models.URLField(null=True)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    venue = models.CharField(max_length=255, null=True)

    dump_dir_path = 'events'
    key_structure = '[user_group]/[date]'

    def __str__(self):
        return self.name

    class Manager(PagesManager):
        def scheduled_in_month(self, year, month):
            return self.filter(date__year=year, date__month=month)

        def future_events(self):
            today = datetime.date.today()
            return self.filter(date__gte=today).order_by('date', 'time')

        def future_events_in_next_month(self):
            today = datetime.date.today()
            thiry_days_time = today + datetime.timedelta(days=30)
            return self.filter(date__gte=today, date__lt=thiry_days_time).order_by('date', 'time')

    objects = Manager()
