from __future__ import absolute_import
from django.shortcuts import render

# Create your views here.
# response json is in the form:
# { 'result' : ['ok'|'fail'],
#     'obj_type' : ['invoice'|'customer'],
#     'obj_attr1' : [value] .....}

import json
from copy import copy
from django.db import transaction, IntegrityError, connection
from django.http import HttpResponse, Http404, HttpResponseNotFound, HttpResponseServerError
from django.core.urlresolvers import resolve
from atomic_test.models import Customer, Invoice
import sys

# @transaction.set_autocommit(False) #, connection('db.sqlite3'))
def superbulk_transactional(request):
    encoder = json.JSONEncoder()
    data_list = json.loads(request.body)
    res_list = []
    # from nose.tools import set_trace; set_trace()
    transaction.atomic(True)
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

    except IntegrityError:
        transaction.rollback()
        return HttpResponse(content=json.dumps({'result': 'fail'}),
                            status=500)
    finally:
        transaction.atomic(False)
    transaction.commit()
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
        http_response = json.dumps({
            'result': 'ok',
            'obj_type': 'invoice',
            'customer_id': data['customer_id'],
            'invoice_no': data['invoice_no']
        })
        return HttpResponse(content=http_response,
                            status=200)
    except Exception as e:
        http_response = json.dumps({
            'result': 'fail',
            'obj_type': 'invoice',
            'customer_id': None, #data['customer_id'],
            'invoice_no': None, #data['invoice_no']
            'reason': e.message
        })
        return HttpResponse(content=http_response, status=500)

def customer(request):
    # from nose.tools import set_trace; set_trace()
    data = json.loads(request.body)
    try:
        test_customer = Customer(data['id'], data['name'])
        test_customer.save()
        http_response = json.dumps({
            'result': 'ok',
            'obj_type': 'customer',
            'id': data['id'],
            'name': data['name'],
            'reason': None
        })
        return HttpResponse(content=http_response,
                            status=200)
    except Exception as e:
        http_response = json.dumps({
            'result': 'fail',
            'obj_type': 'customer',
            'id': None, #data['customer_id'],
            'name': None, #data['invoice_no']
            'reason': e.message
        })
        return HttpResponse(content=http_response,
                            status=500)