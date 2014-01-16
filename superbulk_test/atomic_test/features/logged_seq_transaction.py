from lettuce import *
from django.test.client import Client
import json
from nose.tools import eq_, ok_

from atomic_test.models import Invoice
from utils import clean_db

from utils import before_all, set_post_data, make_request

@before.all
def set_browser():
    before_all()

@step(r'the post data is "(.*)"')
def access_url(step, data):
    set_post_data(data)

@step(r'I post the data to "(.*)"')
def post_data(step, url):
    make_request(url, world.post_data)

@step(r'all individual responses have correct format')
def inserts_worked_as_expected(step):
    data = json.loads(world.response_data)
    for data_object in data:
        dom = json.loads(data_object['content'])
        statuscode = data_object['status_code']
        if int(statuscode) < 400:
            customer_id = dom['customer_id']
            invoice_no = dom['invoice_no']
            ok_(Invoice.objects.filter(customer_id=customer_id, invoice_no=invoice_no))
        elif int(statuscode) >= 400:
            err_message = dom['customer_id']
            assert err_message == None
