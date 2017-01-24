from django.views.generic import DetailView, ListView

from .models import Event, UserGroup


class UserGroupListView(ListView):
    model = UserGroup
    context_object_name = 'groups'


class UserGroupDetailView(DetailView):
    model = UserGroup
    slug_field = 'key'

    def get_context_data(self, object):
        group = object

        return {
            'group': group,
            'next_event': group.next_event(),
            'past_events': group.past_events(),
            'other_future_events': group.other_future_events(),
        }


class EventListView(ListView):
    model = Event
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.future_events()
