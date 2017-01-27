import datetime
import re

from django.db import models
from django_amber.models import ModelWithContent, ModelWithoutContent, PagesManager


class UserGroup(ModelWithoutContent):
    name = models.CharField(max_length=255)
    url = models.URLField(null=True)

    dump_dir_path = 'user-groups'

    def __str__(self):
        return self.name

    class Manager(PagesManager):
        def no_events_scheduled(self, year, month):
            subquery = self.filter(events__date__year=year, events__date__month=month)
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


class NewsItem(ModelWithContent):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    date = models.DateField()

    dump_dir_path = 'news'

    @classmethod
    def fields_from_key(cls, key):
        pattern = '(?P<year>\d\d\d\d)-(?P<month>\d\d)-(?P<day>\d\d)-(?P<slug>.+)'
        match = re.match(pattern, key)
        groups = match.groupdict()
        date = datetime.datetime(int(groups['year']), int(groups['month']), int(groups['day']))
        return {'date': date, 'slug': groups['slug']}

    def __str__(self):
        return self.title

    class Manager(PagesManager):
        def recent_news(self):
            return self.order_by('-date')[:5]

    objects = Manager()
