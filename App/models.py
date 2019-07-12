from __future__ import unicode_literals

from django.contrib.auth import authenticate
from django.db import models
# from db.base_model import BaseModel
from datetime import datetime
from tinymce.models import HTMLField
from django.contrib.auth.models import AbstractUser
# Create your models here.
from stdimage.models import StdImageField
from stdimage.utils import UploadToUUID
from DjangoUeditor.models import UEditorField


class AdminUser(models.Model):
    adminemail = models.CharField(max_length=30,verbose_name='管理员邮箱')
    adminpwd = models.CharField(max_length=40,verbose_name='管理员密码')

class User(models.Model):
    '''用户模型类'''
    uname = models.CharField(max_length=20,verbose_name='用户名')
    upwd= models.CharField(max_length=40,verbose_name='用户密码')
    uemail = models.CharField(max_length=30,verbose_name='用户邮箱')
    phone= models.CharField(max_length=11,null=True,verbose_name='手机号')
    create_time = models.DateTimeField(default=datetime.now,null=True,verbose_name='创建时间')
    class Meta:
        db_table = 'df_user'
        verbose_name = '注册用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.uname



class Address(models.Model):
    '''地址模型类'''
    # user = authenticate(request, username=uname, password=pwd)
    user = models.ForeignKey('User', verbose_name='所属账户')
    receiver = models.CharField(max_length=20, verbose_name='收件人')
    addr = models.CharField(max_length=256, verbose_name='收件地址')
    zip_code = models.CharField(max_length=6, null=True, verbose_name='邮政编码')
    phone = models.CharField(max_length=11, verbose_name='联系电话')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    class Meta:
        db_table = 'df_address'
        verbose_name = '地址'
        verbose_name_plural = verbose_name
class GoodsType(models.Model):
    '''商品类型模型类'''
    name = models.CharField(max_length=20, verbose_name='种类名称')
    logo = models.CharField(max_length=20, verbose_name='标识')
    image = models.ImageField(upload_to='type', verbose_name='商品类型图片')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    class Meta:
        db_table = 'df_goods_type'
        verbose_name = '商品种类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsSKU(models.Model):
    '''商品SKU模型类'''
    status_choices = (
        (0, '下线'),
        (1, '上线'),
    )
    type = models.ForeignKey('GoodsType', verbose_name='商品种类')
    goods = models.ForeignKey('Goods', verbose_name='商品SPU')
    name = models.CharField(max_length=20, verbose_name='商品名称')
    desc = models.CharField(max_length=256, verbose_name='商品简介')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    unite = models.CharField(max_length=20, verbose_name='商品单位')
    image = models.ImageField(upload_to='goods', verbose_name='商品图片')
    stock = models.IntegerField(default=1, verbose_name='商品库存')
    sales = models.IntegerField(default=0, verbose_name='商品销量')
    status = models.SmallIntegerField(default=1, choices=status_choices, verbose_name='商品状态')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    dianji = models.CharField(default=0,max_length=256,verbose_name='点击量')
    class Meta:
        db_table = 'df_goods_sku'
        verbose_name = '商品'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name


class Goods(models.Model):
    '''商品SPU模型类'''
    name = models.CharField(max_length=20, verbose_name='商品SPU名称')
    # 富文本类型:带有格式的文本
    detail = UEditorField(blank=True,width=750,height=300, verbose_name='商品详情')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    class Meta:
        db_table = 'df_goods'
        verbose_name = '商品SPU'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class GoodsImage(models.Model):
    '''商品图片模型类'''
    sku = models.ForeignKey('GoodsSKU', verbose_name='商品')
    image = models.ImageField(upload_to='goods', verbose_name='图片路径')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    class Meta:
        db_table = 'df_goods_image'
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.sku)


class IndexGoodsBanner(models.Model):
    '''首页轮播商品展示模型类'''
    sku = models.ForeignKey('GoodsSKU', verbose_name='商品')
    image = models.ImageField(upload_to='banner', verbose_name='图片')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    class Meta:
        db_table = 'df_index_banner'
        verbose_name = '首页轮播商品'
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.sku)

class IndexTypeGoodsBanner(models.Model):
    '''首页分类商品展示模型类'''
    DISPLAY_TYPE_CHOICES = (
        (0, "标题"),
        (1, "图片")
    )

    type = models.ForeignKey('GoodsType', verbose_name='商品类型')
    sku = models.ForeignKey('GoodsSKU', verbose_name='商品SKU')
    display_type = models.SmallIntegerField(default=1, choices=DISPLAY_TYPE_CHOICES, verbose_name='展示类型')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    class Meta:
        db_table = 'df_index_type_goods'
        verbose_name = "主页分类展示商品"
        verbose_name_plural = verbose_name
    def __str__(self):
        return str(self.type)

class IndexPromotionBanner(models.Model):
    '''首页促销活动模型类'''
    name = models.CharField(max_length=20, verbose_name='活动名称')
    url = models.URLField(verbose_name='活动链接')
    image = models.ImageField(upload_to='banner', verbose_name='活动图片')
    index = models.SmallIntegerField(default=0, verbose_name='展示顺序')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    class Meta:
        db_table = 'df_index_promotion'
        verbose_name = "主页促销活动"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class OrderInfo(models.Model):
    '''订单模型类'''
    PAY_METHODS = {
        '1': "货到付款",
        '2': "微信支付",
        '3': "支付宝",
        '4': '银联支付'
    }

    PAY_METHODS_ENUM = {
        "CASH": 1,
        "ALIPAY": 2
    }

    ORDER_STATUS_ENUM = {
        "UNPAID": 1,
        "UNSEND": 2,
        "UNRECEIVED": 3,
        "UNCOMMENT": 4,
        "FINISHED": 5
    }

    PAY_METHOD_CHOICES = (
        (1, '货到付款'),
        (2, '微信支付'),
        (3, '支付宝'),
        (4, '银联支付')
    )

    ORDER_STATUS = {
        1: '待支付',
        2: '待发货',
        3: '待收货',
        4: '待评价',
        5: '已完成'
    }

    ORDER_STATUS_CHOICES = (
        (1, '待支付'),
        (2, '待发货'),
        (3, '待收货'),
        (4, '待评价'),
        (5, '已完成')
    )

    order_id = models.CharField(max_length=128, primary_key=True, verbose_name='订单id')
    user = models.ForeignKey('User', verbose_name='用户')
    addr = models.ForeignKey('Address', verbose_name='地址')
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=3, verbose_name='支付方式')
    total_count = models.IntegerField(default=1, verbose_name='商品数量')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品总价')
    transit_price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='订单运费')
    order_status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES, default=1, verbose_name='订单状态')
    trade_no = models.CharField(max_length=128, verbose_name='支付编号')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    class Meta:
        db_table = 'df_order_info'
        verbose_name = '订单'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.user


class OrderGoods(models.Model):
    '''订单商品模型类'''
    order = models.ForeignKey('OrderInfo', verbose_name='订单')
    sku = models.ForeignKey('GoodsSKU', verbose_name='商品SKU')
    count = models.IntegerField(default=1, verbose_name='商品数目')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    comment = models.CharField(max_length=256, verbose_name='评论')
    create_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')
    class Meta:
        db_table = 'df_order_goods'
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name
