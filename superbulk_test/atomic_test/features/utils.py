from django.test.client import Client
from lettuce import *

from atomic_test.models import Invoice


def clean_db():
    Invoice.objects.all().delete()


def before_all():
    clean_db()
    world.browser = Client()


def set_post_data(data):
    world.post_data = data


def make_request(url, data=None):
    if data:
        response = world.browser.post(url, world.post_data, content_type='application/json')
        world.response_data = response.content
    else:
        response = world.browser.get(url)
        world.response_data = response.content