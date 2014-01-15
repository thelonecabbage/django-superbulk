from lettuce import *
from lxml import html
from django.test.client import Client
from nose.tools import assert_equals
import json
from atomic_test.models import Customer, Invoice

@before.all
def set_browser():
    world.browser = Client()

@step(r'the post data is "(.*)"')
def access_url(step, data):
    world.post_data = data

@step(r'I post the data to "(.*)"')
def post_data(step, url):
    response = world.browser.post(url, world.post_data, content_type='application/json')
    world.response_data = response.content


@step(r'both inserts are inside the database')
def inserts_worked(step):
    # from nose.tools import set_trace;set_trace()
    data = json.loads(world.response_data)
    for data_object in data:
        dom = json.loads(data_object['content'])
        if dom['obj_type'] == 'customer':
            customer_id = dom['id']
            customer_name = dom['name']
            temp_obj = Customer.objects.get(id=customer_id, name=customer_name)
            assert temp_obj is not None
        else:
            customer_id = dom['customer_id']
            invoice_no = dom['invoice_no']
            temp_obj = Invoice.objects.get(customer_id=customer_id, invoice_no=invoice_no)
            assert temp_obj is not None


@step(r'the post data is "(.*)"')
def access_url(step, data):
    world.post_data = data

@step(r'I post the data to "(.*)"')
def post_data(step, url):
    response = world.browser.post(url, world.post_data, content_type='application/json')
    world.response_data = response.content

@step(r'transaction failed atomically')
def inserts_failed(step):
    # from nose.tools import set_trace; set_trace()
    data = json.loads(world.response_data)
    overall_success = True
    for data_object in data:
        if data['result'] == 'ok':
            overall_success = overall_success and True
        else:
            overall_success = overall_success and False
    # if not overall_success: