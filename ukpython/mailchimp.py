import calendar
from datetime import date
import os

import requests

from django.template.loader import get_template

from ukpython.models import Event, NewsItem, UserGroup

API_KEY = os.getenv('MAILCHIMP_API_KEY')
DATA_CENTRE = API_KEY.split('-')[-1]
BASE_URL = 'https://{}.api.mailchimp.com/3.0/'.format(DATA_CENTRE)
AUTH = ('', API_KEY)

LIST_NAME = 'API Test'
TEMPLATE_NAME = '1 Column'


def get(path, params=None):
    rsp = requests.get(BASE_URL + path, auth=AUTH, params=params)
    rsp.raise_for_status()
    return rsp.json()


def post(path, data=None):
    rsp = requests.post(BASE_URL + path, auth=AUTH, json=data)
    rsp.raise_for_status()
    return rsp.json()


def put(path, data=None):
    rsp = requests.put(BASE_URL + path, auth=AUTH, json=data)
    rsp.raise_for_status()
    return rsp.json()


def get_list_id(list_name=LIST_NAME):
    lists = get('lists')['lists']

    for record in lists:
        if record['name'] == list_name:
            return record['id']


def get_campaign_id(campaign_title):
    campaigns = get('campaigns', {'status': 'save'})['campaigns']

    for record in campaigns:
        if record['settings']['title'] == campaign_title:
            return record['id']


def get_template_id(template_name=TEMPLATE_NAME):
    templates = get('templates', {'count': 1000})['templates']

    for record in templates:
        if record['name'] == template_name:
            return record['id']


def get_or_create_campaign(year, month):
    title = 'UK Python News {}-{:02d}'.format(year, month)
    campaign_id = get_campaign_id(title)

    if campaign_id is not None:
        return campaign_id

    list_id = get_list_id()

    month_name = calendar.month_name[int(month)]
    subject_line = 'UK Python News {} {}'.format(month_name, year)

    data = {
        'type': 'regular',
        'recipients': {'list_id': list_id},
        'settings': {
            'subject_line': subject_line,
            'title': title,
            'from_name': 'PyCon UK',
            'reply_to': 'peter.inglesby@gmail.com',
        },
    }

    return post('campaigns', data)['id']


def update_campaign_content(campaign_id, year, month):
    news_items = NewsItem.objects.for_newsletter(year, month)

    upcoming_events = Event.objects.scheduled_in_month(year, month).order_by('date')
    groups_with_no_events_scheduled = UserGroup.objects.no_events_scheduled(year, month).order_by('name')

    month_name = calendar.month_name[month]
    next_month_name = calendar.month_name[(month + 1) % 12]
    next_month_deadline = date(year, month, 24)
    
    template = get_template('mailchimp-newsletter.html')

    context = {
        'news_items': news_items,
        'upcoming_events': upcoming_events,
        'groups_with_no_events_scheduled': groups_with_no_events_scheduled,
        'month_name': month_name,
        'next_month_name': next_month_name,
        'next_month_deadline': next_month_deadline,
    }

    html = template.render(context)
    template_id = get_template_id()

    data = {
        'html': html,
        'template': {'id': template_id},  # This doesn't actually work
    }

    put('campaigns/{}/content'.format(campaign_id), data)


def update_mailchimp(year, month):
    campaign_id = get_or_create_campaign(year, month)
    update_campaign_content(campaign_id, year, month)
