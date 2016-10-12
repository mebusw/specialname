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
                              {'characters': request.POST.get('characters', 'xyz'),
                               'gender': request.POST.get('gender', 0)},
                              context_instance=RequestContext(request))





# @login_required(login_url=LOGIN_URL)
# def do_create_order(request):
#     request.user.first_name = request.POST.get("first_name")
#     request.user.save()
#     request.user.customer.address = request.POST.get("address")
#     request.user.customer.save()

#     survey_result_id = request.POST.get("survey_result_id")
#     order = Order.objects.create(user=request.user, survey_result=SurveyResult.objects.get(pk=survey_result_id))

#     total_price = 0
#     product_count = int(request.POST.get("product_count", 0))
#     for i in xrange(product_count):
#         product = Product.objects.get(pk=request.POST.get("product_id" + str(i)))
#         amount = int(request.POST.get("product_amount" + str(i)))
#         # print product, amount
#         if amount > 0:
#             order_item = OrderItem.objects.create(order=order, product=product, amount=amount)
#             total_price += product.price * amount

#     order.total_price = total_price
#     order.discount_price = total_price
#     order.out_trade_no = _generate_req_seq()

#     # ####### point rules #######
#     try:
#         referrer = Customer.objects.get(user__username=request.user.customer.referrer_mobile)
#         getcontext().prec = 16
#         order.discount_price = total_price * Decimal(0.8)
#     except Exception, e:
#         print e
#     finally:
#         print '========', total_price, type(total_price), order.discount_price, type(order.discount_price)
#     # ###########################

#     order.save()

#     return HttpResponseRedirect(reverse('peggy.views.order', kwargs={"order_id": order.id}))


# @login_required(login_url=LOGIN_URL)
# def payment_wap(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     return HttpResponse(AlipayWap().make(order.out_trade_no, u"PEGGYS实验室定制", str(order.discount_price)))


# @csrf_exempt
# def paid_wap(request):
#     params = request.GET.dict()
#     # print params
#     is_correct_sign = AlipayWap().is_correct_sign(params)

#     order = Order.objects.get(out_trade_no=params['out_trade_no'])

#     return render_to_response('peggy/paid.html',
#                               {'out_trade_no': params["out_trade_no"], 'result': params['result'],
#                                'discount_price': order.discount_price,
#                                'is_correct_sign': is_correct_sign}, context_instance=RequestContext(request))


# @csrf_exempt
# def paid_notify_wap(request):
#     params = request.POST.dict()
#     verify_result = AlipayWap().notify_call(params, verify=True)
#     print "ASYNC_wap verifying alipay: ", verify_result, params

#     if verify_result == 'success':
#         try:
#             t = ET.fromstring(params['notify_data'].encode('utf8'))
#             out_trade_no = t.find('out_trade_no').text
#             print "change order state for ", out_trade_no
#             order = Order.objects.get(out_trade_no=out_trade_no)
#             order.state = Order.PAID
#             order.pay_date = datetime_safe.datetime.now()
#             order.save()

#             referrer = Customer.objects.get(user__username=order.user.customer.referrer_mobile)
#             referrer.point += int(order.total_price) * 2
#             referrer.save()

#         except Exception, e:
#             print e
#     return HttpResponse(verify_result)


# @login_required(login_url=LOGIN_URL)
# def order(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     order_items = OrderItem.objects.filter(order=order)
#     return render_to_response('peggy/order.html', {'order': order, 'order_items': order_items},
#                               context_instance=RequestContext(request))
