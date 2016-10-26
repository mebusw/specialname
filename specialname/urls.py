"""uperform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import patterns, url, include
from views import *


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^jsonp$', jsonp),
    url(r'^$', index),
    url(r'^order/(?P<order_id>\d+)$', order),
    url(r'^payment$', payment),
    url(r'^payment_wap$', payment_wap),
    url(r'^paid_wap$', paid_wap),
    url(r'^paid_notify_wap$', paid_notify_wap),

    url(r'^payment_paypal$', payment_paypal),
    url(r'^payment_return$', payment_return),
]


