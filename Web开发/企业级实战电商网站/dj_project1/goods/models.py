from django.db import models


# Create your models here.

class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)  # 分类名称
    isDelete = models.BooleanField(default=False)  # #是否删除

    class Meta:
        db_table = 'typeinfo'  #指定数据表名

    def __str__(self):
        return self.ttitle


class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20)  # 商品名称
    gpic = models.ImageField(upload_to='goods')  # 图片
    gprice = models.DecimalField(max_digits=5, decimal_places=2)  # #单价
    isDelete = models.BooleanField(default=False)  # #是否删除
    gunit = models.CharField(max_length=20, default='500g')  # #单位
    gclick = models.IntegerField()  # #点击量，人气
    gjianjie = models.CharField(max_length=200)  # #简介
    gkucun = models.IntegerField()  # #库存量
    gcontent = models.TextField()  # #描述
    gtype = models.ForeignKey(TypeInfo)  # #类型

    class Meta:
        db_table = 'goodsinfo'  #指定数据表名


    def __str__(self):
        return self.gtitle
