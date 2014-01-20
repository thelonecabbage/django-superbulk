from __future__ import absolute_import
from copy import copy
import json
from urlparse import urlparse

from django.core.urlresolvers import resolve
from django.db import transaction
from django.http import HttpResponse, QueryDict
from django.views.decorators.http import require_http_methods

class MultipleHTTPError(Exception):
    """Raised when transaction fails
    message: json

    """
@require_http_methods(["POST"])
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
    if isinstance(data, list):
        failfast = False
    elif isinstance(data, dict):
        failfast = data.get('failfast', False)
        data = data['content']
    else:
        raise NotImplementedError("Individual requests have body "
                                  "of unsupported json type(other than list and dict)")
    return failfast, data


def request_handler(request, data_list, failfast=False):
    """Handles a list of requests in json form

    @params: request: Passed in from the view that calls
                    the method
            data_list: list of the json form requests
            failfast: bool var that determines if this
                     will fail on first error
    @return: bool : if one transaction failed
            list : list of request responses

    """
    res_list = []
    one_failed = False
    for data in data_list:
        if failfast and one_failed:
            break
        uri = urlparse(data['uri'])
        view, args, kwargs = resolve(uri.path)
        this_request = copy(request)
        this_request._body = data['body']
        this_request.method = data['method']
        this_request.GET = QueryDict(uri.query)
        kwargs['request'] = this_request
        try:
            res = view(*args, **kwargs)
        except:
            one_failed = True
        if res.status_code >= 400:
            one_failed = True
        res_list.append({
            'status_code': res.status_code,
            'headers': res._headers,
            'content': res.content
        })
    return one_failed, res_list




def superbulk_atom(request):
    """Performs transactions in request atomically

    @return: json encoded response
    @raises: MultipleHttpError

    """
    encoder = json.JSONEncoder()
    failfast, data_list = failfast_jsonloads(request.body)
    one_failed, res_list = request_handler(request, data_list, failfast=failfast)
    if one_failed:
        raise MultipleHTTPError(encoder.encode(res_list))
    return HttpResponse(
        encoder.encode(res_list), content_type='application/json')


@require_http_methods(["POST"])
def superbulk(request):
    """Performs multiple transactions passed in
    from request

    @return: list of results from executing
            transactions

    """
    encoder = json.JSONEncoder()
    data_list = json.loads(request.body)
    one_failed, res_list = request_handler(request, data_list)
    return HttpResponse(
        encoder.encode(res_list), content_type='application/json')
