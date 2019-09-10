from django.conf.urls import include, url
from goods.views import *

# good  商品
urlpatterns = [
    # 展示首页
    url(r'^$', index),

    #展示商品列表
    url(r'^g_list(\d+)/$', g_list),

    #展示商品详情页
    url(r'^detail(\d+)/$', detail),

]