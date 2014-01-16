from lettuce import *
from django.test.client import Client
import json

from atomic_test.models import Invoice

def clean_db():
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
        dom = json.loads(data_object['content'])
        statuscode = data_object['status_code']
        if int(statuscode) < 400:
            customer_id = dom['customer_id']
            invoice_no = dom['invoice_no']
            temp_obj = Invoice.objects.get(customer_id=customer_id, invoice_no=invoice_no)
            assert temp_obj is not None
        elif int(statuscode) >= 400:
            err_message = dom['result']
            assert err_message == 'fail'
