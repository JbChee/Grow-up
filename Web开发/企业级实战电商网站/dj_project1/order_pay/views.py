from django.shortcuts import render, redirect
from django.conf import settings
import os
from alipay import AliPay
from users.models import *
import time

from django.db import transaction

# Create your views here.


from django.http import JsonResponse

# 生成支付宝对象
alipay = AliPay(appid=settings.ALIPAY_APPID,
                app_notify_url=None,
                app_private_key_path=os.path.join(settings.STATICFILES_DIRS[0], 'app_private_key.pem'),
                alipay_public_key_path=os.path.join(settings.STATICFILES_DIRS[0], 'alipay_public_key.pem'),
                sign_type='RSA2',
                debug=True, )


def order_index(request):
    if request.session.get('id'):
        dict1 = request.GET
        cid = dict1.getlist('cid')
        cart_list = Cart.objects.filter(id__in=cid)
        lens = len(cart_list)



        user_id = request.session.get('id')  # 获取用户id
        user = UserAddressInfo.objects.filter(user_id=user_id)[0]  # 用户地址信息

        str1 = f'{user.uaddress}({user.uname}收){user.uphone}'  # 构建收货信息

        content = {'title': '订单', 'cart_list': cart_list, 'infos': str1,'lens':lens}
        return render(request, 'order_pay/place_order.html', content)
    else:
        return redirect('/login/')


@transaction.atomic
def do_order(request):
    pay_style = request.GET.get('pay_style')
    cids = request.GET.getlist('cids')  # 商品id
    total_price = request.GET.get('total_price')  # 商品总价

    uid = request.session.get('id')
    useradd = UserAddressInfo.objects.filter(user_id=uid)[0]  # 用户

    # 开启事务
    sid = transaction.savepoint()
    # 创建订单主表
    order = OrderInfo()
    order.oid = str(int(time.time() * 1000)) + str(uid)  # 构建订单编号
    order.user_id = uid
    order.ototal = total_price
    order.oaddress = useradd.uaddress
    order.save()

    cart_list = Cart.objects.filter(id__in=cids)  # 购物车对象

    total = 0
    isOK = True
    for cart in cart_list:
        if cart.count <= cart.cgood.gkucun:
            detail = OrderDetailInfo()  # 订单详情页
            detail.order = order
            detail.goods_id = cart.cgood_id
            detail.price = cart.cgood.gprice
            detail.count = cart.count
            detail.save()

            total += detail.count * detail.price
            cart.cgood.gkucun -= cart.count
            cart.cgood.save()
            cart.delete()  # 删除购物车对象
        else:
            # 只要有一个支付失败，isOK == False
            isOK = False
            break
    if isOK:
        order_total = total

        if pay_style == 'cash':
            order.oIsPay = 1
            order.save()
            transaction.savepoint_commit(sid)  # 提交事务
            return JsonResponse({'res': 1})
        else:
            order_id = order.oid  # 订单编号
            total_pay = order_total
            order_string = alipay.api_alipay_trade_page_pay(
                out_trade_no=order_id,
                total_amount=str(total_pay),
                subject=f'python班{order_id}',
                return_url='http://127.0.0.1:8000/order/check_pay/?order_id=' + order_id,
                notify__url='http://127.0.0.1:8000/order/check_pay/?order_id=' + order_id,
            )
            alipay_url = settings.ALIPAY_URL + '?' + order_string

            return JsonResponse({'res': 3, 'pay_url': alipay_url, 'order_id': order_id})
    else:
        transaction.set_rollback(sid)
        return JsonResponse({'res': 0})


def check_pay(request):
    order_id = request.GET.get('order_id')
    order = OrderInfo.objects.get(oid=order_id)  # 订单对象

    while True:
        time.sleep(1)
        response = alipay.api_alipay_trade_query(order_id)  # 验证支付状态
        # 获取响应里的属性
        code = response.get('code')
        trade_status = response.get('trade_status')
        if code == '10000' and trade_status == 'TRADE_SUCCESS':
            order.oIsPay = 1
            order.save()
            return redirect('info')
        elif code == '40004' or (code == '10000' and trade_status == 'WAIT_BUYER_PAY'):
            continue
        else:
            return JsonResponse({'code': 0})
