from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from goods.models import *


# Create your views here.

# 商城首页
def index(request):
    type_name = TypeInfo.objects.all()  # 种类
    goods_list = []
    for i in type_name:
        # id_goods = GoodsInfo.objects.filter(gtype_id=i)[0:4]
        # id_goods = GoodsInfo.objects.filter(gtype_id=i).order_by('-gclick')[0:4]
        id_goods = i.goodsinfo_set.order_by('-id')[0:4]
        goods_list.append([i, id_goods])

    context = {'title': '天天生鲜',
               'welcome': '欢迎光临',
               'user': 'Hongkuang',
               'goods_list': goods_list,
               'type_name': type_name,

               }

    return render(request, 'goods/index.html', context)


# 商品列表
from django.core.paginator import Paginator


def g_list(request, id):
    types = TypeInfo.objects.all()  # 所有商品类别

    type_name = TypeInfo.objects.filter(id=id)[0]  # 商品所在类别

    all_tygoods = type_name.goodsinfo_set.all()  # 同一类别所有信息

    recomment_goods = all_tygoods.order_by('-id')[:2]  # 推荐数据

    # 排序
    all_tygoods.order_by('-id')  # 默认排序
    sort = request.GET.get('sort', 1)
    # print('sort', sort)

    if sort == '2':  # 价格
        all_tygoods.order_by('-gprice')
    if sort == '3':  # 点击量
        all_tygoods.order_by('-gclick')

    # 分页
    page_num = request.GET.get('page', 1)

    p = Paginator(all_tygoods, 5)  # 每页数据 为 2
    # page_range = p.page_range  #返回页数列表 【1，2，3....】
    now_page = int(page_num)
    # print(now_page)
    page = p.page(now_page)  # 当前页数据  是Page()实例对象
    # 自定义 页数列表
    page_range = list(range(max(now_page - 2, 1), now_page)) + list(range(now_page, min(now_page + 2, p.num_pages) + 1))
    # print(page_range)
    # [ 4, 5, 6, 7, 8 ]

    if (page_range[0] - 1 > 2):  # 头部 省略
        page_range.insert(0, '...')
    if (p.num_pages - page_range[-1] > 2):  # 尾部 省略
        page_range.append('...')

    if (page_range[0] != 1):  # 头部添加 1
        page_range.insert(0, 1)
    if (page_range[-1] != p.num_pages):  # 尾部添加 最大页数
        page_range.append(p.num_pages)
    # print(page_range)

    # 分类导航
    class_name = ['fruit', 'seafood', 'meet', 'egg', 'vegetables', 'ice']
    zip_obj = []
    name_class_obj = zip(types, class_name)
    for i, j in name_class_obj:
        zip_obj.append([i, j])

    content = {'type_name': type_name.ttitle,
               'all_tygoods': all_tygoods,
               'recomment_goods': recomment_goods,
               'page': page,
               'page_range': page_range,
               'title': '商品列表',
               'zip_obj': zip_obj,
               'sort': sort,
               }
    return render(request, 'goods/list.html', content)


import random
import queue  # 队列

goods_id = []
def detail(request, id):
    print(type(id))
    # 生成数据
    type_name = TypeInfo.objects.all()              # 商品的所有类别
    good_obj = GoodsInfo.objects.filter(id=id)[0]  # 获取当前商品对象
    type_id = good_obj.gtype_id                     #获取当前商品的类别
    print('type_id',type_id)

    # 每次单击，点击量加一
    good_obj.gclick += 1
    good_obj.save()

    # 获取推荐商品对象
    rm_goods = GoodsInfo.objects.filter(gtype_id=type_id).order_by('-gclick')[:2]


    # 导航条类名
    class_name = ['fruit', 'seafood', 'meet', 'egg', 'vegetables', 'ice']

    zip_obj = []
    name_class_obj = zip(type_name, class_name)
    for i, j in name_class_obj:
        zip_obj.append([i, j])

    # print(zip_obj)
    content = {
        'title':'商品详情',
        'zip_obj': zip_obj,
        'good_obj': good_obj,
        'rm_goods': rm_goods,

    }
    response = render(request, 'goods/detail.html', content)

    # 设置最近浏览的商品

    # q = queue.Queue(5)

    # id = int(id)
    str(goods_id).replace("\054",",")
    if len(goods_id) < 5:

        goods_id.append(id)  # 入队
        response.set_cookie('goods', goods_id)
        print('detail--------',goods_id)
        return response
    else:  # 满了
        goods_id.pop(0)  # 先删除第一个
        goods_id.append(id)   #然后再添加
        response.set_cookie('goods', goods_id)
        print(goods_id)

        return response
