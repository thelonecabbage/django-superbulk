from __future__ import absolute_import
import json
import sys

from django.http import HttpResponse
from django.forms.models import model_to_dict

from atomic_test.models import Invoice

def invoice(request):
    """Performs the actual database actions

    return: response with 200 status -> ok
                          500 status -> fail

    """

    data = json.loads(request.body)
    try:
        test_invoice = Invoice(data['customer_id'], data['invoice_no'])
        test_invoice.save()
        http_response = model_to_dict(test_invoice)
        code = 200
    except Exception as e:
        http_response = {
            'customer_id': None,
            'invoice_no': None,
            'reason': e.message
        }
        code = 500
    return HttpResponse(content=json.dumps(http_response), status=code)