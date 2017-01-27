import calendar

from django.shortcuts import render

from .models import Event, UserGroup


def index(request):
    context = {'events': Event.objects.future_events_in_next_month()}
    return render(request, 'ukpython/index.html', context)


def user_groups(request):
    context = {'groups': UserGroup.objects.order_by('name')}
    return render(request, 'ukpython/user_groups.html', context)


def user_group(request, key):
    group = UserGroup.objects.get(key=key)
    context = {
        'group': group,
        'next_event': group.next_event(),
        'past_events': group.past_events(),
        'other_future_events': group.other_future_events(),
    }
    return render(request, 'ukpython/user_group.html', context)


def future_events(request):
    context = {'events': Event.objects.future_events()}
    return render(request, 'ukpython/events.html', context)


def user_groups_with_no_events_scheduled(request, year, month):
    context = {
        'groups': UserGroup.objects.no_events_scheduled(year, month).order_by('name'),
        'month_name': calendar.month_name[int(month)],
        'year': year,
    }
    return render(request, 'ukpython/user_groups_with_no_events_scheduled.html', context)
