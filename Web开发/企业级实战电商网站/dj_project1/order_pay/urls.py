from django.conf.urls import include, url

from order_pay.views import *


urlpatterns = [
    # 展示订单支付页面
    url(r'^$', order_index),

    url(r'^check_pay/$', check_pay),
    url(r'^do_order/$', do_order),

]