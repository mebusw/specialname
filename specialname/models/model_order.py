#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

import time
from django.utils.datetime_safe import datetime

from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_CHOICES = ((GENDER_MALE, '男'), (GENDER_FEMALE, '女'),)

    user = models.OneToOneField(User)
    birthday = models.DateTimeField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=4, choices=GENDER_CHOICES, blank=True, null=True)
    weixin = models.CharField(max_length=20, blank=True, null=True)
    alipay = models.CharField(max_length=40, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    avatar_url = models.URLField(max_length=200, blank=True, null=True)
    referrer_mobile = models.CharField(max_length=20, blank=True, null=True, default='')
    point = models.BigIntegerField(default=0)
    create_date = models.DateTimeField(max_length=100, blank=True, null=True, auto_now_add=True)
    update_date = models.DateTimeField(max_length=100, blank=True, null=True)
    last_checkin_time = models.DateTimeField(max_length=100, blank=True, null=True, auto_now_add=True)

    class Meta:
        app_label = 'sn'

    @property
    def age(self):
        today_aware = datetime.today()
        return (today_aware - self.birthday).days / 365 + 1

    @property
    def username(self):
        return self.user.username

    @property
    def first_name(self):
        return self.user.first_name

    def __unicode__(self):
        return u'%s @ %s - referred by %s' % (self.user.username, self.point, self.referrer_mobile)

class Order(models.Model):
    CREATED = 'CREATED'
    PAID = 'PAID'
    PRODUCED = 'PRODUCED'
    SENT = 'SENT'
    DELIVERED = 'DELIVERED'
    CONSUMED = 'CONSUMED'
    CANCELLED = 'CANCELLED'
    STATE_CHOICES = ((CREATED, '已创建'), (PAID, '已支付'), (PRODUCED, '已调配'), (SENT, '已发货'), (DELIVERED, '已签收'),
                     (CONSUMED, '已使用'), (CANCELLED, '已取消'))

    EXPRESS_CHOICES = (('shunfeng', '顺丰'), ('yuantong', '圆通'), ('zhongtong', '中通') , ('shentong', '申通'), ('tiantian', '天天快递'))

    user = models.ForeignKey(User)
    survey_result = models.ForeignKey(SurveyResult, null=True)
    out_trade_no = models.CharField(max_length=255, null=True, blank=True)
    express_no = models.CharField(max_length=255, null=True, blank=True)
    express_vendor = models.CharField(max_length=255, choices=EXPRESS_CHOICES, null=True, blank=True)
    total_price = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    discount_price = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    pay_date = models.DateTimeField(null=True, blank=True)
    deliver_date = models.DateTimeField(null=True)
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default=CREATED)

    class Meta:
        app_label = 'sn'

    def __unicode__(self):
        return u'￥%s (%s) for %s - %s - %s' % (
            self.discount_price, self.total_price, self.user.username, self.state, self.out_trade_no)


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=16, decimal_places=2, default=0)

    class Meta:
        app_label = 'sn'

    def __unicode__(self):
        return u'%s / ￥%s' % (self.name, self.price)


class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    amount = models.IntegerField(max_length=10, default=0)

    class Meta:
        app_label = 'sn'

    def __unicode__(self):
        return u'%s %s x%s @ %s' % (self.product.name, self.product.price, self.amount, self.order.id)
