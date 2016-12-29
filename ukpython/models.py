from django.db import models
from django_amber.models import ModelWithoutContent


class UserGroup(ModelWithoutContent):
    name = models.CharField(max_length=255)
    url = models.URLField(null=True)

    dump_dir_path = 'user-groups'

    def __str__(self):
        return self.name
