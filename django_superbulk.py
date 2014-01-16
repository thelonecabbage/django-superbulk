from __future__ import absolute_import
from copy import copy
import json

from django.core.urlresolvers import resolve
from django.db import transaction
from django.http import HttpResponse

class MultipleHTTPError(Exception):
    """Raised when transaction fails
    message: json

    """
def superbulk_transactional(request):
    """Executes all transactions in the request atomically
    wraps superbulk_atom call in a transaction block

    @return: json formed response

    """
    try:
        with transaction.commit_on_success():
            return superbulk_atom(request)
    except MultipleHTTPError as e:
        return HttpResponse(str(e), content_type='application/json')

def failfast_jsonloads(body):
    """Loads request body based on format
    in order to extract failfast variable,
    and preserve back compatibility.

    @params: body : string
    @return: tuple(bool, list)

    """
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
    """Performs transactions in request atomically

    @return: json encoded response
    @raises: MultipleHttpError
    """
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
    """Performs multiple transactions passed in
    from request

    @return: list of results from executing
            transactions

    """
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
