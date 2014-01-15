from lettuce import *
from lxml import html
from django.test.client import Client
from nose.tools import assert_equals
import json
from atomic_test.models import Customer, Invoice

def clean_db():
    Customer.objects.all().delete()
    Invoice.objects.all().delete()

@before.all
def set_browser():
    clean_db()
    world.browser = Client()

@step(r'the post data is "(.*)"')
def access_url(step, data):
    world.post_data = data

@step(r'I post the data to "(.*)"')
def post_data(step, url):
    response = world.browser.post(url, world.post_data, content_type='application/json')
    world.response_data = response.content

@step(r'everything worked fine with logging')
def inserts_worked_as_expected(step):
    data = json.loads(world.response_data)
    for data_object in data:
        dom = data_object['content']
        statuscode = data_object['status_code']
        if int(statuscode) < 400:
            customer_id = dom['customer_id']
            customer_name = dom['name']
            temp_obj = Customer.objects.get(id=customer_id, name=customer_name)
            assert temp_obj is not None
        elif int(statuscode) >= 400:
            err_message = dom['result']
            assert err_message == 'fail'