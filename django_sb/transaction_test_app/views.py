from __future__ import absolute_import
from django.shortcuts import render

# Create your views here.


import json
from copy import copy
from django.db import transaction, IntegrityError
from django.http import HttpResponse, Http404, HttpResponseNotFound, HttpResponseServerError
from django.core.urlresolvers import resolve
from transaction_test_app.models import Invoice, Customer
import sys

@transaction.set_autocommit(False)
def superbulk_transactional(request):
    encoder = json.JSONEncoder()
    data_list = json.loads(request.body)
    res_list = []
    from nose.tools import set_trace; set_trace()
    # transaction.atomic(True)
    try:
        # with transaction.atomic:
        for data in data_list:
            view, args, kwargs = resolve(data['uri'])
            this_request = copy(request)

            this_request._body = data['body']
            this_request.method = data['method']
            kwargs['request'] = this_request
            try:
                res = view(*args, **kwargs)
            except Exception:
                raise IntegrityError
            if res.status_code >= 400:
                raise IntegrityError
            res_list.append({
                'status_code': res.status_code,
                'headers': res._headers,
                'content': res.content
            })
            transaction.commit()
    except IntegrityError:
        transaction.rollback()

    return HttpResponse(
        encoder.encode(res_list), content_type='application/json')

def superbulk(request):
    encoder = json.JSONEncoder()
    data_list = json.loads(request.body)
    res_list = []

    for data in data_list:
        view, args, kwargs = resolve(data['uri'])
        this_request = copy(request)

        this_request._body = data['body']
        this_request.method = data['method']
        kwargs['request'] = this_request
        # from nose.tools import set_trace; set_trace()
        try:
            res = view(*args, **kwargs)
        except Exception as e:
            print e.message
            sys.exit(1)
        res_list.append({
            'status_code': res.status_code,
            'headers': res._headers,
            'content': res.content
        })

    return HttpResponse(
        encoder.encode(res_list), content_type='application/json')

def invoice(request):
    data = json.loads(request.body)
    try:
        test_invoice = Invoice(data['customer_id'], data['invoice_no'])
        test_invoice.save()
        return HttpResponse(content="<div><h1>Record added</h1>"
                                    "<p>invoice</p>"
                                    "<h2>Customer Id:<h3>%(customer_id)s</h3></h2>"
                                    "<h2>Invoice Number:<h3>%(invoice_no)s</h3></h2></div>" % data,
                            status=200)
    except Exception as e:
        return HttpResponse(content="<h1>Error on insertion</h1>"
                                    "<br />"
                                    "<h2>%s</h2>" % e.message, status=500)

def customer(request):
    # from nose.tools import set_trace; set_trace()
    data = json.loads(request.body)
    try:
        test_customer = Customer(data['id'], data['name'])
        test_customer.save()
        return HttpResponse(content="<div><h1>Record added</h1>"
                                    "<p>customer</p>"
                                    "<h2>Customer Id:<h3>%(id)s</h3></h2>"
                                    "<h2>Invoice Number:<h3>%(name)s</h3></h2></div>" % data,
                            status=200)
    except Exception as e:
        return HttpResponse(content="<h1>Error on insertion</h1>"
                                    "<br />"
                                    "<h2>%s</h2>" % e.message,
                            status=500)