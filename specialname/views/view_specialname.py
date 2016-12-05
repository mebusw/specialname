# -*- coding: utf-8 -*-
import hashlib
from django.contrib.auth.models import Permission
from django.shortcuts import render_to_response, get_object_or_404, redirect
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
import urllib
from specialname.models import *
import paypalrestsdk as paypal
from algorithm import *


def jsonp(request):
    return HttpResponse(json.dumps({'read': [True, None, 1, 2, 3]}), content_type="application/json")


def index(request):
    return render_to_response('specialname/index.html',
                              {},
                              context_instance=RequestContext(request))


def order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # order_item = OrderItem.objects.filter(order=order)[0]

    return render_to_response('specialname/paid.html',
                              {'paymentId': request.GET.get("paymentId", ""),
                               # 'hostname': urllib.quote(settings.HOSTNAME),
                               'order': order}, context_instance=RequestContext(request))


def _generate_req_seq(aux_id=''):
    return datetime.now().strftime('%Y%m%d%H%M%S') + str(aux_id)


def _create_order():
    product, created = Product.objects.get_or_create(pk=1, defaults={'name': 'One Name For Life', 'price': 2.99,
                                                                     'unit': 'USD'})
    order = Order.objects.create()

    amount = 1
    order_item = OrderItem.objects.create(order=order, product=product, amount=amount)
    # TODO reduce all OrderItem
    total_price = amount * order_item.product.price

    order.total_price = total_price
    order.discount_price = total_price
    order.currency = order_item.product.currency
    order.save()

    return order


def payment(request):
    return render_to_response('specialname/payment.html',
                              {'characters': request.POST.get('characters', 'xyz'),
                               'gender': request.POST.get('gender', 0),
                               'product': get_object_or_404(Product, pk=1),
                               },
                              context_instance=RequestContext(request))


def payment_wap(request):
    order = _create_order()
    order.client_email = request.POST['client_email']
    order.client_name = request.POST['client_name']
    order.client_chars = request.POST['client_chars']
    order.client_gender = request.POST['client_gender']
    order.pay_channel = order.ALIPAY
    order.out_trade_no = _generate_req_seq()
    order.save()

    return HttpResponse(AlipayWap().make(order.out_trade_no, u"SpecialName", str(order.discount_price)))


@csrf_exempt
def paid_wap(request):
    params = request.POST.dict()
    is_correct_sign = AlipayWap().is_correct_sign(params)

    order = Order.objects.get(out_trade_no=params['out_trade_no'])
    #TODO
    order.deliverable = '王二狗 赵淑芬'
    order.state = Order.PAID
    order.pay_date = datetime_safe.datetime.now()
    order.save()

    return render_to_response('specialname/paid.html',
                              {'out_trade_no': request.GET["out_trade_no"], 'result': request.GET['result'],
                               'discount_price': order.discount_price,
                               'is_correct_sign': is_correct_sign,
                               'order': order}, context_instance=RequestContext(request))


@csrf_exempt
def paid_notify_wap(request):
    params = request.POST.dict()
    verify_result = AlipayWap().notify_call(params, verify=True)
    print "ASYNC_wap verifying alipay: ", verify_result, params

    if verify_result == 'success':
        try:
            t = ET.fromstring(params['notify_data'].encode('utf8'))
            out_trade_no = t.find('out_trade_no').text
            order = Order.objects.get(out_trade_no=out_trade_no)
            order.state = Order.PAID
            order.pay_date = datetime_safe.datetime.now()
            order.save()

        except Exception, e:
            print e
    return HttpResponse(verify_result)


def payment_paypal_create(request):
    order = _create_order()
    order.client_email = request.POST['client_email']
    order.client_name = request.POST['client_name']
    order.client_chars = request.POST['client_chars']
    order.client_gender = request.POST['client_gender']
    order.pay_channel = order.PAYPAL
    order.save()

    paypal.configure({
        "mode": "live" if settings.IS_PRODUCTION_ENV else "sandbox",
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET,
    })

    payment = paypal.Payment({
        "intent": "sale",

        # Payer
        # A resource representing a Payer that funds a payment
        # Payment Method as 'paypal'
        "payer": {
            "payment_method": "paypal"},

        # Redirect URLs
        "redirect_urls": {
            "return_url": settings.HOSTNAME + "/payment/paypal/return",
            "cancel_url": settings.HOSTNAME + "/"},

        # Transaction
        # A transaction defines the contract of a
        # payment - what is the payment for and who
        # is fulfilling it.
        "transactions": [{

            # ItemList
            "item_list": {
                "items": [{
                    "name": "Chinese Name",
                    "sku": "item",
                    "price": str(order.orderitem_set.all()[0].product.price),
                    "currency": order.currency,
                    "quantity": 1}]},

            # Amount
            # Let's you specify a payment amount.
            "amount": {
                "total": str(order.discount_price),
                "currency": order.currency},
            "description": "This is the payment transaction description."}]})

    # Create Payment and return status
    if payment.create():
        print("Payment[%s] created successfully" % (payment.id))
        order.paypal_payment_id = payment.id
        order.save()
        # Redirect the user to given approval url
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = str(link.href)
                print("Redirect for approval: %s" % (redirect_url))
                return redirect(redirect_url)
    else:
        print("Error while creating payment:")
        print(payment.error)
        return HttpResponse('Error while creating payment: %s' % payment.error)


def payment_paypal_return(request):
    paypal.configure({
        "mode": "live" if settings.IS_PRODUCTION_ENV else "sandbox",
        "client_id": settings.PAYPAL_CLIENT_ID,
        "client_secret": settings.PAYPAL_CLIENT_SECRET,
    })

    payment = paypal.Payment.find(request.GET['paymentId'])
    if payment.execute({"payer_id": request.GET['PayerID']}):
        print("Payment execute successfully")

        order = Order.objects.get(paypal_payment_id=request.GET['paymentId'])
        order.paypal_payer_id = request.GET['PayerID']
        order.state = Order.PAID
        order.pay_date = datetime_safe.datetime.now()
        order.deliverable = deliver_name(order.client_chars, order.client_gender)
        print order.deliverable
        order.save()

        return render_to_response('specialname/paid.html',
                                  {'paymentId': request.GET["paymentId"],
                                   'discount_price': order.discount_price,
                                   'order': order}, context_instance=RequestContext(request))
    else:
        print(payment.error)
        return HttpResponse(payment.error)


