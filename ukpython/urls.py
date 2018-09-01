from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^groups/$', views.user_groups, name='user-groups'),
    url(r'^groups/(?P<key>[\w-]+)/$', views.user_group, name='user-group'),
    url(r'events/$', views.future_events, name='future-events'),
    url(r'^groups-with-no-events-scheduled/(?P<year>\d+)/(?P<month>\d+)/$', views.user_groups_with_no_events_scheduled, name='user-groups-with-no-events-scheduled'),
    url(r'news/$', views.news, name='news'),
    url(r'news/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[\w-]+)/$', views.news_item, name='news-item'),
    url(r'^(?P<key>.*?)/$', views.page_view, name='page'),
    url(r'^static/(?P<path>.*)$', views.serve_static),
]
