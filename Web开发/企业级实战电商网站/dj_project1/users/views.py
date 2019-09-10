from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from users.models import *
from goods.models import *
from users.forms import *
from hashlib import sha1, md5
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


# 登录

def login(request):
    # from_path = request.META.get('HTTP_REFERER', '/')
    # 路径保存在session中
    # request.session['LoginFrom'] = from_path
    # 用户session存在，之间登录
    if request.session.get('username'):
        return redirect('/')
    else:
        print('return login')
        return render(request, 'users/login.html')


@csrf_exempt
def login_check(request):
    # 获取表单数据
    print('-------start--------')
    result = {'status': 'error', 'datas': '11'}
    if request.method == 'POST':
        # 获取数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        print(remember)
        print(username)

        # 获取数据库数据
        try:
            user = UserInfo.objects.filter(uname=username)[0]  # 根据用户名查找
            print(user)
        except:
            result['datas'] = '用户名不存在'
        else:
            if user:  # 找到用户名

                if user.upw == take_sha1(password):  # 密码正确
                    result['status'] = 'success'
                    result['datas'] = '登录成功'
                    # 设置cookie 和 session
                    print('-----------next cookie ---------')
                    response = JsonResponse(result)
                    response.set_cookie('username', user.uname)
                    request.session['username'] = username
                    request.session['id'] = user.id  # 设置session id
                    # from_path = request.META.get('HTTP_REFERER', '/')
                    # 路径保存在session中
                    # request.session['LoginFrom'] = from_path

                    if remember == 'true':
                        # 记住登录状态
                        response.set_cookie('remUser', True, 3600)
                        # 设置cookie
                        response.set_cookie('username', username, 3600)
                        # response.set_cookie('password', password,3600)
                    else:
                        response.delete_cookie('remUser')
                        response.delete_cookie('username')
                        # response.delete_cookie('password')
                    return response
                else:  # 密码不对
                    result['datas'] = '用户名或密码错误'
                    response = JsonResponse(result)
                    if remember == 'true':
                        # 记住登录状态
                        response.set_cookie('remUser', True, 3600)  # 如果为 true ,在前端获取cookie值，设置为输入框的值
                        # 设置cookie
                        response.set_cookie('username', username, 3600)
                        # response.set_cookie('password', password,3600)
                    else:
                        response.delete_cookie('remUser')
                        response.delete_cookie('username')
                        # response.delete_cookie('password')

                    return response

    return JsonResponse(result)


# 注册
def take_sha1(content):
    hashs = sha1()  # 创建hash加密实例
    hashs.update(content.encode())  # hash加密
    result = hashs.hexdigest()  # 得到加密结果
    return result


def register(request):
    # from_path = request.META.get('HTTP_REFERER', '/')
    # 路径保存在session中
    # request.session['RegisterFrom'] = from_path
    form = UserData()
    if request.method == 'POST':
        form = UserData(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            namefilter = UserInfo.objects.filter(uname=username)
            if len(namefilter) >= 1:
                return render(request, 'users/register.html', {'form': form, 'errors1': '用户已存在，请重新注册'})  # 用户已存在
            else:
                password1 = form.cleaned_data['password1']
                password = take_sha1(password1)  # 加密密码
                email = form.cleaned_data['email']

                # 写入数据 到数据库
                user = UserInfo.objects.create(uname=username, upw=password, uemail=email)
                user.save()
                request.session['username'] = username
                namefilter = UserInfo.objects.filter(uname=username)
                request.session['id'] = namefilter[0].id  # 设置session id
                # return render(request,'goods/index.html',{'username':username})
                return redirect('/user_center_info')
        else:   #信息不合法
            return redirect('/register')
    else:
        form = UserData()
        return render(request, 'users/register.html', {'form': form})

def delete_cookie(request):
    request.session.flush()
    return redirect('/')


# 个人中心信息
def user_center_info(request):
    if request.session.get('username'):
        user_id = request.session.get('id')  # 获取用户id
        goods_id = request.COOKIES.get('goods')  # 获取商品id列表

        print('user_info++++++++++++', goods_id)
        print(type(goods_id))

        goods_list = []
        if len(goods_id) >=1 :
            for u_id in eval(goods_id):
                good = GoodsInfo.objects.filter(id=u_id)[0]
                goods_list.insert(0, good)

            # 查看一下用户的个人信息
            user = UserInfo.objects.filter(id=user_id)[0]
            print()
            content = {
                'title': '个人信息',
                'goods_list': goods_list,
                'user': user,
            }

            return render(request, 'users/user_center_info.html', content)
        else:
            user = UserInfo.objects.filter(id=user_id)[0]
            print()
            content = {
                'title': '个人信息',
                'user': user,
            }

            return render(request, 'users/user_center_info.html', content)



    else:
        return redirect('/login')


# 全部订单
from django.core.paginator import Paginator
def user_center_order(request):
    if request.session.get('id'):
        user_id = request.session.get('id')
        order_ispays = OrderInfo.objects.filter(user_id = user_id, oIsPay=1)
        order_notpays = OrderInfo.objects.filter(user_id = user_id, oIsPay=0)
        all_orders = OrderInfo.objects.filter(user_id = user_id).order_by('oIsPay')

        print(order_ispays)
        cart_goods = Cart.objects.filter(cuser=user_id)

        # 分页
        page_num = request.GET.get('page', 1)

        p = Paginator(all_orders, 2)  # 每页数据 为 2
        page_range = p.page_range  #返回页数列表 【1，2，3....】
        now_page = int(page_num)
        # print(now_page)
        page = p.page(now_page)  # 当前页数据  是Page()实例对象



        content = {
            'title': '全部订单',
            # 'order_ispays':order_ispays,
            # 'order_notpays':order_notpays,
            'page_range': page_range,
            'page':page,
        }
        return render(request, 'users/user_center_order.html', content)
    else:
        return redirect('/login')

# 收获地址
def user_center_site(request):
    user_id = request.session.get('id')  # 获取用户id
    user = UserInfo.objects.filter(id=user_id)[0]
    content = {
        'title': '收货地址',
        'err_msg': 2,
        'user': user,
    }
    if request.method == 'POST':
        dict = request.POST

        uname = dict.get('uname')
        uphone = dict.get('uphone')
        postcard = dict.get('postcard')
        text = dict.get('text')
        if uname:
            u_addr_obj = UserAddressInfo()
            u_addr_obj.uname = uname
            u_addr_obj.uphone = uphone
            u_addr_obj.postcard = postcard
            u_addr_obj.uaddress = text
            u_addr_obj.user_id = user_id
            u_addr_obj.save()
            return render(request, 'users/user_center_info.html', content)
        else:
            content['err_msg'] = 1
            return render(request, 'users/user_center_site.html', content)
    else:
        content['err_msg'] = 3
        return render(request, 'users/user_center_site.html', content)


# 购物车
def cart(request):
    if request.session.get('id'):
        user_id = request.session.get('id')
        cart_goods = Cart.objects.filter(cuser=user_id)
        lens = len(cart_goods)
        #购物车数量小于1

        content = {
            'title': '购物车',
            'cart_goods': cart_goods,
            'lens':lens,
        }
        return render(request, 'users/cart.html', content)
    else:
        return redirect('/login')


from django.db.models import Sum


@csrf_exempt
def add_goods(request):
    user_id = request.session.get('id')
    dict = request.POST
    # 获取数据
    count = int(dict.get('count', 0))
    good_id = dict.get('goods_id')
    #查询商品
    cart_goods = Cart.objects.filter(cuser_id=user_id, cgood_id=good_id)
    print('cart_goods',cart_goods)
    if cart_goods:  # 商品存在
        cart_good = cart_goods[0]
        cart_good.count += count
        cart_good.save()

    else:  # 商品不存在
        cart = Cart()
        cart.cuser_id = int(user_id)
        cart.cgood_id = int(good_id)
        cart.count = count
        cart.save()
    c = Cart.objects.filter(cuser_id=user_id).aggregate(Sum('count'))
    json = {'msg': 1, 'count': c.get('count__sum')}
    print('json',json)
    return JsonResponse(json)

@csrf_exempt
def count(request):
    user_id = request.session.get('id')
    c = Cart.objects.filter(cuser_id=user_id).aggregate(Sum('count'))
    return JsonResponse({'msg': 1, 'count': c.get('count__sum')})

#编辑购物车商品数量
def goods_edit(request):
    cid = request.GET.get('cid')
    count = request.GET.get('count')
    cart = Cart.objects.get(id=cid)
    cart.count = count
    cart.save()
    return JsonResponse({'msg':1})

#删除购物车商品
def del_good(request):
    cid = request.GET.get('cid')
    cart = Cart.objects.get(id=cid)
    cart.delete()
    return JsonResponse({'msg':1})

