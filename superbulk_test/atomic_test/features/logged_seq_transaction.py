from lettuce import *
from django.test.client import Client
import json
from nose.tools import eq_, ok_

from atomic_test.models import Invoice
from utils import clean_db

from utils import before_all, set_post_data, make_request


@step(r'all individual responses have correct format')
def inserts_worked_as_expected(step):
    data = json.loads(world.response_data)
    for data_object in data:
        json_obj = json.loads(data_object['content'])
        statuscode = data_object['status_code']
        if int(statuscode) < 400:
            customer_id = json_obj['customer_id']
            invoice_no = json_obj['invoice_no']
            ok_(Invoice.objects.filter(customer_id=customer_id, invoice_no=invoice_no))
        elif int(statuscode) >= 400:
            err_message = json_obj['reason']
            ok_(err_message, "Failed response did not return reason")
