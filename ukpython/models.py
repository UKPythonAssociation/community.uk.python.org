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


class Event(ModelWithoutContent):
    user_group = models.ForeignKey(UserGroup)
    name = models.CharField(max_length=255)
    url = models.URLField(null=True)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    venue = models.CharField(max_length=255, null=True)

    dump_dir_path = 'events'
    key_structure = '[user_group]/[date]'

    def __str__(self):
        return self.name
