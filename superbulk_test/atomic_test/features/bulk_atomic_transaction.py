import json
from nose.tools import eq_, ok_

from lettuce import *


from atomic_test.models import Invoice

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
        if 'customer_id' in data_object.keys():
            temp = json.loads(data_object['content'])
            customer_id = temp['customer_id']
            invoice_no = temp['invoice_no']
            ok_(not Invoice.objects.filter(customer_id=customer_id, invoice_no=invoice_no))

@step(r'transaction stops after first failure')
def insert_failed_break(step):
    data = json.loads(world.response_data)
    assert len(data) == 2