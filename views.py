from __future__ import absolute_import

import json
from copy import copy
from urlparse import urlparse

from django.http import HttpResponse, QueryDict
from django.core.urlresolvers import resolve


def superbulk(request):
    encoder = json.JSONEncoder()
    data_list = json.loads(request.body)
    res_list = []

    for data in data_list:
        uri = urlparse(data['uri'])
        view, args, kwargs = resolve(uri.path)
        this_request = copy(request)

        this_request._body = data['body']
        this_request.method = data['method']
        this_request.GET = QueryDict(uri.query)
        kwargs['request'] = this_request

        res = view(*args, **kwargs)
        res_list.append({
            'status_code': res.status_code,
            'headers': res._headers,
            'content': res.content
        })

    return HttpResponse(
        encoder.encode(res_list), content_type='application/json')
