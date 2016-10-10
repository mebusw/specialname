# -*- coding: utf-8 -*-
import hashlib
from django.contrib.auth.models import Permission
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.utils import datetime_safe
import urllib2, urllib
import json
import time
from random import random


def jsonp(request):
    return HttpResponse(json.dumps({'read': [True, None, 1, 2, 3]}), content_type="application/json")


def index(request):
    return render_to_response('specialname/index.html',
                              {},
                              context_instance=RequestContext(request))

def payment(request):
    return render_to_response('specialname/payment.html',
                              {'chars': request.POST.get('characters', 'xyz')},
                              context_instance=RequestContext(request))
