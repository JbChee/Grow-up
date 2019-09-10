from django.conf.urls import  url
from users.views import *

#输入网址   user/......
urlpatterns = [

    url(r'^login/$', login),  #进入登录页面
    url(r'^login_check/$', login_check),   #进入登录验证函数


    url(r'^register/', register),  #进入注册页面
    # url(r'^register_check/', register_check),  #进入注册验证函数
    url(r'delete_cookie/', delete_cookie),

    #个人信息
    url(r'^user_center_info/$', user_center_info,name='info'),
    #订单
    url(r'^user_center_order/$', user_center_order),
    #收获地址
    url(r'^user_center_site/$', user_center_site),

    #购物车
    url(r'^cart/$', cart),
    url(r'^add_goods/$', add_goods),
    url(r'^count/$', count),
    url(r'^goods_edit/$', goods_edit),
    url(r'^del_good/$', del_good),



]