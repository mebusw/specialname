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
from specialname.lib.alipaylib import AlipayWap
import xml.etree.ElementTree as ET
from specialname.models import *

def jsonp(request):
    return HttpResponse(json.dumps({'read': [True, None, 1, 2, 3]}), content_type="application/json")


def index(request):
    return render_to_response('specialname/index.html',
                              {},
                              context_instance=RequestContext(request))


def order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    return render_to_response('specialname/order.html', {'order_id': order.id, 'email': order.email,
                                                        'client_name': order.client_name,
                                                        'deliverable': order.deliverable},
                              context_instance=RequestContext(request))


def _generate_req_seq(aux_id=''):
    return datetime.now().strftime('%Y%m%d%H%M%S') + str(aux_id)


def payment(request):
    product, created = Product.objects.get_or_create(pk=1, defaults={'name': 'One Name For Life', 'price': 0.01})
    order = Order.objects.create()

    total_price = 0
    product_count = 1
    amount = 1
    order_item = OrderItem.objects.create(order=order, product=product, amount=amount)
    total_price += product.price * amount

    order.total_price = total_price
    order.discount_price = total_price
    order.out_trade_no = _generate_req_seq()
    order.save()

    # return HttpResponseRedirect(reverse('specialname.views.order', kwargs={"order_id": order.id}))
    return render_to_response('specialname/payment.html',
                          {'characters': request.POST.get('characters', 'xyz'),
                           'gender': request.POST.get('gender', 0),
                           'order_id': order.id},
                          context_instance=RequestContext(request))


def payment_wap(request):
    order = get_object_or_404(Order, id=request.POST['order_id'])
    order.email = request.POST['email']
    order.client_name = request.POST['client_name']
    order.save()

    return HttpResponse(AlipayWap().make(order.out_trade_no, u"SpecialName", str(order.discount_price)))


@csrf_exempt
def paid_wap(request):
    params = request.GET.dict()
    # print params
    is_correct_sign = AlipayWap().is_correct_sign(params)

    order = Order.objects.get(out_trade_no=params['out_trade_no'])
    order.deliverable = '王二狗 赵淑芬'
    order.save()

    return render_to_response('specialname/paid.html',
                              {'out_trade_no': params["out_trade_no"], 'result': params['result'],
                               'discount_price': order.discount_price,
                               'is_correct_sign': is_correct_sign,
                               'deliverable': order.deliverable}, context_instance=RequestContext(request))


@csrf_exempt
def paid_notify_wap(request):
    params = request.POST.dict()
    verify_result = AlipayWap().notify_call(params, verify=True)
    print "ASYNC_wap verifying alipay: ", verify_result, params

    if verify_result == 'success':
        try:
            t = ET.fromstring(params['notify_data'].encode('utf8'))
            out_trade_no = t.find('out_trade_no').text
            print "change order state for ", out_trade_no
            order = Order.objects.get(out_trade_no=out_trade_no)
            order.state = Order.PAID
            order.pay_date = datetime_safe.datetime.now()
            order.save()

        except Exception, e:
            print e
    return HttpResponse(verify_result)



