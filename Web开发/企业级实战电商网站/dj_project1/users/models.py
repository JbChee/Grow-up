from django.db import models

# Create your models here.

#用户注册信息
class UserInfo(models.Model):
    uname = models.CharField(max_length=20)    #用户名
    upw = models.CharField(max_length=50)      #密码
    uemail = models.EmailField(max_length=30)      #邮箱
    isValid = models.BooleanField(default=True)   #是否被禁用
    isActive = models.BooleanField(default=False)  #是否被激活  发送邮件后才能激活
    create_time = models.DateField(auto_now_add=True)  #用户创建时间

    class Meta:
        db_table = 'userinfo'  #指定数据表名

    def __str__(self):
        return self.uname


#用户个人信息
class UserAddressInfo(models.Model):
    uname=models.CharField(max_length=20)  #收件人
    uaddress=models.CharField(max_length=100)    #收货地址
    postcard = models.CharField(max_length=11)  # 邮编
    uphone=models.CharField(max_length=11)  #手机电话
    user=models.ForeignKey('UserInfo')  #用户

    class Meta:
        db_table = 'userAddressInfo'  #指定数据表名

    def __str__(self):
        return self.uname

#用户的购物车
class Cart(models.Model):
    cuser = models.ForeignKey('UserInfo')            #用户
    cgood = models.ForeignKey('goods.GoodsInfo')     #用户的商品
    count = models.IntegerField()                    #购物车商品数量

    class Meta:
        db_table = 'cart'  #指定数据表名

    def __str__(self):
        return self.cuser

class OrderInfo(models.Model):
    oid=models.CharField(max_length=20, primary_key=True)    #订单编号  当前时间+用户编号
    user=models.ForeignKey('UserInfo')              #订单用户
    odate=models.DateTimeField(auto_now_add=True)   #下单日期
    oIsPay=models.BooleanField(default=False)           #是否支付
    ototal=models.DecimalField(max_digits=6,decimal_places=2)     #金额总计
    oaddress=models.CharField(max_length=150)  #收获地址

    class Meta:
        db_table = 'orderinfo'  #指定数据表名

    def __str__(self):
        return self.oid



class OrderDetailInfo(models.Model):
    goods=models.ForeignKey('goods.GoodsInfo')  #商品
    order=models.ForeignKey('OrderInfo')    #订单
    price=models.DecimalField(max_digits=5,decimal_places=2)  #价格
    count=models.IntegerField()      #数量


    class Meta:
        db_table = 'orderdetailinfo'  #指定数据表名


    def __str__(self):
        return self.goods




