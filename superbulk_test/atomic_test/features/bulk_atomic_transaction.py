import json
from nose.tools import eq_, ok_

from lettuce import *


from atomic_test.models import Invoice
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


@step(r'both inserts are inside the database')
def inserts_worked(step):
    data = json.loads(world.response_data)
    for data_object in data:
        dom = json.loads(data_object['content'])
        customer_id = dom['customer_id']
        invoice_no = dom['invoice_no']
        ok_(Invoice.objects.filter(customer_id=customer_id, invoice_no=invoice_no))

@step(r'transaction failed atomically')
def inserts_failed(step):
    data = json.loads(world.response_data)
    for data_object in data:
        temp = json.loads(data_object['content'])
        customer_id = temp['customer_id']
        invoice_no = temp['invoice_no']
        ok_(not Invoice.objects.filter(customer_id=customer_id, invoice_no=invoice_no))

@step(r'transaction stops after first failure')
def insert_failed_break(step):
    data = json.loads(world.response_data)
    assert len(data) == 2