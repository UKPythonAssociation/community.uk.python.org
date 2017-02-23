import calendar
import datetime

from django.shortcuts import render

from .models import Event, NewsItem, UserGroup


def index(request):
    context = {
        'events': Event.objects.future_events_in_next_month(),
        'news_items': NewsItem.objects.recent_news()
    }
    return render(request, 'ukpython/index.html', context)


def user_groups(request):
    context = {'groups': UserGroup.objects.all()}
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
        'groups': UserGroup.objects.no_events_scheduled(year, month),
        'month_name': calendar.month_name[int(month)],
        'year': year,
    }
    return render(request, 'ukpython/user_groups_with_no_events_scheduled.html', context)


def news(request):
    context = {
        'news_items': NewsItem.objects.all()
    }
    return render(request, 'ukpython/news.html', context)


def news_item(request, year, month, day, slug):
    date = datetime.date(int(year), int(month), int(day))
    news_item = NewsItem.objects.get(slug=slug, date=date)

    context = {
        'news_item': news_item,
    }
    return render(request, 'ukpython/news_item.html', context)
