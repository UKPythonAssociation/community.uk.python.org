from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^groups/$', views.UserGroupListView.as_view(), name='user-groups'),
    url(r'^groups/(?P<slug>[\w-]+)/$', views.UserGroupDetailView.as_view(), name='user-group'),
]
