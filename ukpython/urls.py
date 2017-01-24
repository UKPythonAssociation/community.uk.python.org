from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^groups/$', views.user_groups, name='user-groups'),
    url(r'^groups/(?P<key>[\w-]+)/$', views.user_group, name='user-group'),
    url(r'events/$', views.future_events, name='future-events'),
]
