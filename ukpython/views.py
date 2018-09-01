import calendar
import datetime
import os
import posixpath

from django.contrib.staticfiles import finders
from django.http import Http404
from django.shortcuts import render
from django.utils.six.moves.urllib.parse import unquote
from django.views import static

from .models import Event, NewsItem, Page, UserGroup


def index(request):
    context = {
        'events': Event.objects.future_events_in_next_month(),
        'news_items': NewsItem.objects.for_website(num_items=5),
    }
    return render(request, 'ukpython/index.html', context)


def page_view(request, key):
    page = Page.objects.get(key=key)

    assert page.content_format in ['html', 'md'], 'Page content must use HTML or Markdown'

    context = {
        'content': page.content,
        'content_format': page.content_format,
        'title': page.title,
    }

    return render(request, 'ukpython/page.html', context)


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
        'news_items': NewsItem.objects.for_website()
    }
    return render(request, 'ukpython/news.html', context)


def news_item(request, year, month, day, slug):
    date = datetime.date(int(year), int(month), int(day))
    news_item = NewsItem.objects.get(slug=slug, date=date)

    context = {
        'news_item': news_item,
    }
    return render(request, 'ukpython/news_item.html', context)


def serve_static(request, path, insecure=False, **kwargs):
    """
    This is copied from Django's contrib.staticfiles.views to remove the DEBUG
    check.

    We don't need to check DEBUG since we never actually serve the site with
    Django.

    Serve static files below a given point in the directory structure or
    from locations inferred from the staticfiles finders.
    To use, put a URL pattern such as::
        from django.contrib.staticfiles import views
        url(r'^(?P<path>.*)$', views.serve)
    in your URLconf.
    It uses the django.views.static.serve() view to serve the found files.
    """
    normalized_path = posixpath.normpath(unquote(path)).lstrip('/')
    absolute_path = finders.find(normalized_path)
    if not absolute_path:
        if path.endswith('/') or path == '':
            raise Http404("Directory indexes are not allowed here.")
        raise Http404("'%s' could not be found" % path)
    document_root, path = os.path.split(absolute_path)
    return static.serve(request, path, document_root=document_root, **kwargs)
