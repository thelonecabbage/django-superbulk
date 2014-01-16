from __future__ import absolute_import
from copy import copy
import json
import sys

from django.core.urlresolvers import resolve
from django.db import transaction, IntegrityError, connection
from django.http import HttpResponse, Http404, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render

from atomic_test.models import Customer, Invoice

class MultipleHTTPError(Exception):
    """ """

def superbulk_transactional(request):
    """ """
    try:
        with transaction.commit_on_success():
            return superbulk_atom(request)
    except MultipleHTTPError as e:
        return HttpResponse(str(e), content_type='application/json')

def failfast_jsonloads(body):
    data = json.loads(body)
    if type(data) == list:
        return False, json.loads(body)
    elif type(data) == dict:
        if 'failfast' in data.keys():
            if data['failfast'] == 'True':
                return True, data['content']
            else:
                return False, data['content']


def superbulk_atom(request):
    encoder = json.JSONEncoder()
    failfast, data_list = failfast_jsonloads(request.body)
    res_list = []
    one_failed = False
    for data in data_list:
        view, args, kwargs = resolve(data['uri'])
        this_request = copy(request)

        this_request._body = data['body']
        this_request.method = data['method']
        kwargs['request'] = this_request
        try:
            res = view(*args, **kwargs)
        except:
            one_failed = True
            if failfast:
                break
        if res.status_code >= 400:
            one_failed = True
            if failfast:
                break
        res_list.append({
            'status_code': res.status_code,
            'headers': res._headers,
            'content': res.content
        })

    if one_failed:
        raise MultipleHTTPError(json.dumps(res_list))
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
        try:
            res = view(*args, **kwargs)
        except:
            pass
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