from django.shortcuts import render

# Create your views here.
import json
from copy import copy
from django.db import transaction, IntegrityError
from django.http import HttpResponse, Http404, HttpResponseNotFound, HttpResponseServerError
from django.core.urlresolvers import resolve
# from models import Invoice, Customer
import sys


def superbulk(request):
    return HttpResponse("Hello")