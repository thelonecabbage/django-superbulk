from __future__ import absolute_import

import json
from copy import copy

from django.http import HttpResponse
from django.core.urlresolvers import resolve


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

        res = view(*args, **kwargs)
        res_list.append({
            'status_code': res.status_code,
            'headers': res._headers,
            'content': res.content
        })

    return HttpResponse(
        encoder.encode(res_list), content_type='application/json')
