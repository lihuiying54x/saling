#coding=utf-8
from random import randint

from django.contrib.auth import authenticate
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from hashlib import sha1
# Create your views here.
# from App.forms import UserForm
from django_redis import get_redis_connection
from haystack.views import SearchView

from App import user_decorator
from App.models import *
# GoodsInfo
    # TypeInfo,
from django.urls import reverse

# from shengxian.App.forms import UserForm
from App.sms import send_sms
from shengxian.settings import SMSCONFIG


def register(request):
    return render(request,'register.html')

def register_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 =post.get('cpwd')
    uemail = post.get('email')
    if upwd!=upwd2:
        return redirect('/app/register/')
    uphone = post.get('phone')

    # code = post.get('code')
    # if code != request.session.get('smscode'):
    #     return redirect('/app/register/')
    s1 = sha1()
    s1.update(upwd.encode('utf8'))
    upwd3 = s1.hexdigest()

    user = User()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.phone = uphone
    user.save()
    return redirect('/app/index/')

def getCode(request):
    if request.method == 'POST':
        num = randint(100000,999999)
        request.session['smscode'] = str(num)
        phone = request.POST.get('phone')
        send_sms(phone,{'number':str(num)},**SMSCONFIG)
        return JsonResponse({'code':1,'msg':'ok'})

def sms(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        print(code,request.session.get('smscode'))
        if code == request.session.get('smscode'):
            return redirect(reverse('app:index'))
    return render(request,'message.html')

def register_exist(request):
    uname = request.GET.get('uname')
    count = User.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})


def login(request):

    uname = request.COOKIES.get('uname','')
    return render(request, 'login.html', context = {'title': '用户登录', 'error_name':0, 'error_pwd':0, 'uname': uname})

def login_handle(request):
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)
    users = User.objects.filter(uname=uname)

    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd.encode("utf8"))
        if s1.hexdigest() == users[0].upwd:
            url = request.COOKIES.get('url','/app/index/')
            red = HttpResponseRedirect(url)

            # 记住用户名
            if jizhu != 0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uname','', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:

            return render(request, 'login.html', context = {'title': '用户登录', 'error_name':0, 'error_pwd':1, 'uname':uname, 'upwd':upwd})
    else:
        return render(request, 'login.html', context = {'title': '用户登录', 'error_name':1, 'error_pwd':0, 'uname': uname, 'upwd': upwd})


def logout(request):
    request.session.flush()
    return redirect(reverse('app:index'))
    # del request.session['user_id']
    # del request.session['user_name']
    # return redirect('/')




# def index(request):
#     return render(request,'index.html')

@user_decorator.login
def info(request):
    user_email = User.objects.get(id=request.session['user_id']).uemail
    user_phone = User.objects.get(id=request.session['user_id']).phone
    goods_ids1=request.session.get(str(request.session['user_id']),'')
    goods_list = []
    for goods_id in goods_ids1:
        goods_list.append(GoodsSKU.objects.get(id=int(goods_id)))
    context = {'title':'用户中心',
               'user_name':request.session['user_name'],
               'user_email': user_email,
               'user_phone':user_phone,
               'goods_list':goods_list,
            }
    return render(request, 'user_center_info.html', context)
#
@user_decorator.login
def order(request):     #全部订单
    return render(request, 'user_center_order.html', context= {'title': '用户中心'})


@user_decorator.login
def site(request):      #收货地址
    user = User.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.receiver = post.get('receiver')
        user.addr = post.get('addr')
        user.zip_code = post.get('zip_code')
        user.phone = post.get('phone')
        user.save()
    context = {'title': '用户中心', 'user': user}
    return render(request, 'user_center_site1.html', context)


# def detail(request, id):        #详情页    #商品id
#     good = GoodsSKU.objects.get(id=int(id))
#     good.sales = good.sales + 1     #点击量
#     good.save()
#     news = good.type.goodssku_set.order_by('-id')[0:2]
#     context = {
#         'title':good.type.name,
#         'goods':good,
#         'news':news,
#         'id': id,
#     }
#     response = render(request, 'detail.html', context)
#
#     #记录最近浏览,在用户中心使用
#     if request.session.has_key('user_id'):   #判断是否已经登录
#         key=str(request.session.get('user_id'))
#         goods_ids=request.session.get(key,'')
#         # print(type(goods_ids))
#         # print(goods_ids)
#         goods_id = str(good.id)  # 将int型转化为str类型
#         if goods_ids != '':  # 判断是否有浏览记录,如果则继续判断
#             # goods_ids = goods_ids.split(',')  # 以逗号分隔切片    切片后为list型
#             if goods_ids.count(goods_id) >= 1:  # 如果已经存在,删除掉
#                 goods_ids.remove(goods_id)
#             goods_ids.insert(0, goods_id)  # 添加到第一个
#             if len(goods_ids) >= 6:  # 如果超过6个则删除最后一个
#                 del goods_ids[5]
#         else:
#             goods_ids = []
#             goods_ids.append(goods_id)
#         # print(type(goods_ids))
#         # print(goods_ids)
#         request.session[key]=goods_ids
#     return response

# # from haystack.views import SearchView
# # class MySearchView(SearchView):
# #     def extra_context(self):
# #         context=super(MySearchView,self).extra_context()
# #         context['title']='搜索'
# #         context['guest_cart']=1
# #         return context
#
# from haystack.view import SearchView
from shengxian.settings import HAYSTACK_SEARCH_RESULTS_PER_PAGE
#
class MySearchView(SearchView):
    def build_page(self):
        #分页重写
        context=super(MySearchView, self).extra_context()   #继承自带的context
        try:
            page_no = int(self.request.GET.get('page', 1))
        except Exception:
            return HttpResponse("Not a valid number for page.")

        if page_no < 1:
            return HttpResponse("Pages should be 1 or greater.")
        a =[]
        for i in self.results:
            a.append(i.object)
        paginator = Paginator(a, HAYSTACK_SEARCH_RESULTS_PER_PAGE)
        # print("--------")
        # print(page_no)
        page = paginator.page(page_no)
        return (paginator,page)

    def extra_context(self):
        context = super(MySearchView, self).extra_context()  # 继承自带的context
        context['title']='搜索'
        return context


def detail(request, goods_id):
    types = GoodsType.objects.all()
    sku = GoodsSKU.objects.get(id=goods_id)
    sku_orders = OrderGoods.objects.filter(sku=sku).exclude(comment='')
    news = GoodsSKU.objects.filter(type=sku.type).order_by('-create_time')[0:2]
    # sku.dianji = sku.dianji + 1     #点击量
    sku.save()
    # user = request.user
    cart_count = 0
    # news = good.type.goodssku_set.order_by('-id')[0:2]
    context = {
        'title':sku.type.name,
        'sku':sku,
        'types':types,
        'sku_order':sku_orders,
        'news':news,
        'cart_count':cart_count
    }


    #记录最近浏览,在用户中心使用
    if request.session.has_key('user_id'):   #判断是否已经登录
        key=str(request.session.get('user_id'))
        goods_ids=request.session.get(key,'')
        # print(type(goods_ids))
        # print(goods_ids)
        goods_id = str(sku.id)  # 将int型转化为str类型
        if goods_ids != '':  # 判断是否有浏览记录,如果则继续判断
            # goods_ids = goods_ids.split(',')  # 以逗号分隔切片    切片后为list型
            if goods_ids.count(goods_id) >= 1:  # 如果已经存在,删除掉
                goods_ids.remove(goods_id)
            goods_ids.insert(0, goods_id)  # 添加到第一个
            if len(goods_ids) >= 6:  # 如果超过6个则删除最后一个
                del goods_ids[5]
        else:
            goods_ids = []
            goods_ids.append(goods_id)
        # print(type(goods_ids))
        # print(goods_ids)
        request.session[key]=goods_ids
    return render(request, 'detail1.html', context)

def login1(request):
    return render(request, 'login1.html')


def list(request,type,page_num):
    sort = request.GET.get('sort', 'default')
    try:
        page_num = int(page_num)
    except Exception:
        page_num = 1
    types = GoodsType.objects.all()
    type = GoodsType.objects.get(id=type)
    if sort == 'price':
        skus = GoodsSKU.objects.filter(type=type).order_by('price')
    elif sort == 'sales':
        skus = GoodsSKU.objects.filter(type=type).order_by('-sales')
    else:
        skus = GoodsSKU.objects.filter(type=type)

    page_manage = Paginator(skus, 5)

    try:
        page = page_manage.page(page_num)
    except EmptyPage:
        page = page_manage.page(1)
    new_products = GoodsSKU.objects.filter(type=type).order_by('-id')[:2]
    # 控制页码显示5页
    total_page_num = page_manage.num_pages
    if total_page_num < 5:
        show_nums = range(1, total_page_num + 1)
    elif page_num <= 3:
        show_nums = range(1, 6)
    elif total_page_num - page_num <= 2:
        show_nums = range(page_num - 4, total_page_num + 1)
    else:
        show_nums = range(page_num - 2, page_num + 3)
    # show_nums = range(10)
    context = {
        'types': types,
        'page': page,
        'new_products': new_products,
        'current_type': type,
        'sort': sort,
        'show_nums': show_nums,
    }
    return render(request, 'list2.html', context)


def index(request):
    types = GoodsType.objects.all()
    banners = IndexGoodsBanner.objects.all().order_by('-id')[0:4]
    promotion = IndexPromotionBanner.objects.all().order_by('index')
    for type in types:
        word_show = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')[0:4]
        pic_show = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')[0:4]
        type.word_show = word_show
        type.pic_show = pic_show
    context = {
        'title': '首页',
        'types': types,
        'banners': banners,
        'promotion': promotion,
    }
    return render(request, 'index1.html', context)

@user_decorator.login
def cart(request):
    user = User.objects.get(id=request.session['user_id'])
    conn = get_redis_connection('default')
    cart_key = 'cart_%d'%user.id
    cart_dict = conn.hgetall(cart_key)
    skus = []
    total_count = 0
    total_price = 0
    for sku_id,count in cart_dict.items():
        sku = GoodsSKU.objects.get(id = sku_id)
        amount = sku.price*int(count)
        sku.amount = amount
        sku.append(sku)
        total_count += int(count)
        total_price += amount
    context = {'total_count':total_count,
                   'total_price':total_price,
                   'skus':skus}
    return render(request,'cart.html',context)

@user_decorator.login
def add(request):
    user = User.objects.get(id=request.session['user_id'])
    sku_id = request.POST.get('sku_id')
    count = request.POST.get('count')
    if not all([sku_id,count]):
        return JsonResponse({'res':1,'errmsg':'数据不完整'})
    try:
        count = int(count)
    except Exception as e:
        return JsonResponse({'res':2,'errmsg':'商品数目出错'})
    try:
        sku = GoodsSKU.objects.get(id=sku_id)
    except GoodsSKU.DoesNotExist:
        # 商品不存在
        return JsonResponse({'res': 3, 'errmsg': '商品不存在'})
    conn = get_redis_connection('default')
    cart_key = 'cart_%d'%user.id
    cart_count = conn.hget(cart_key,sku_id)
    if cart_count:
        count += int(cart_count)
        if count >sku.stock:
            return JsonResponse({'res':4, 'errmsg':'商品库存不足'})
        conn.hset(cart_key,sku_id,count)
        total_count = conn.hlen(cart_key)
        return JsonResponse({'res':5,'total_count':total_count,'message':'添加成功'})

@user_decorator.login
def update(request):
    user = User.objects.get(id=request.session['user_id'])
    sku_id = request.POST.get('sku_id')
    count = request.POST.get('count')
    if not all([sku_id, count]):
        return JsonResponse({'res': 1, 'errmsg': '数据不完整'})
    try:
        count = int(count)
    except Exception as e:
        # 数目出错
        return JsonResponse({'res': 2, 'errmsg': '商品数目出错'})
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            # 商品不存在
            return JsonResponse({'res': 3, 'errmsg': '商品不存在'})

        conn = get_redis_connection('default')
        cart_key = 'cart_%d'%user.id
        if count > sku.stock:
            return JsonResponse({'res': 4, 'errmsg': '商品库存不足'})
        conn_hset(cart_key,sku_id,count)
        total_count = 0
        vals = conn.hvals(cart_key)
        for val in vals:
            total_count += int(val)
        return JsonResponse({'res': 5, 'total_count': total_count, 'message': '更新成功'})


@user_decorator.login
def delete(request):
    user = User.objects.get(id=request.session['user_id'])
    sku_id = request.POST.get('sku_id')
    if not sku_id:
        return JsonResponse({'res':1, 'errmsg':'无效的商品id'})

    try:
        sku = GoodsSKU.objects.get(id = sku_id)
    except GoodsSKU.DoesNotExist:
        return JsonResponse({'res':2, 'errmsg':'商品不存在'})
    conn = get_redis_connection('default')
    cart_key = 'cart_%d' % user.id
    conn.hdel(cart_key, sku_id)
    total_count = 0
    vals = conn.hvals(cart_key)
    for val in vals:
        total_count += int(val)
    return JsonResponse({'res': 3, 'total_count': total_count, 'message': '删除成功'})



def place_order(request):
    user = request.user
    # 获取参数sku_ids
    sku_ids = request.POST.getlist('sku_ids')  # [1,26]

    # 校验参数
    if not sku_ids:
        # 跳转到购物车页面
        return redirect(reverse('app:cart'))

    conn = get_redis_connection('default')
    cart_key = 'cart_%d' % user.id

    skus = []
    # 保存商品的总件数和总价格
    total_count = 0
    total_price = 0
    # 遍历sku_ids获取用户要购买的商品的信息
    for sku_id in sku_ids:
        # 根据商品的id获取商品的信息
        sku = GoodsSKU.objects.get(id=sku_id)
        # 获取用户所要购买的商品的数量
        count = conn.hget(cart_key, sku_id)
        # 计算商品的小计
        amount = sku.price * int(count)
        # 动态给sku增加属性count,保存购买商品的数量
        sku.count = count
        # 动态给sku增加属性amount,保存购买商品的小计
        sku.amount = amount
        # 追加
        skus.append(sku)
        # 累加计算商品的总件数和总价格
        total_count += int(count)
        total_price += amount

    # 运费:实际开发的时候，属于一个子系统
    transit_price = 10  # 写死

    # 实付款
    total_pay = total_price + transit_price

    # 获取用户的收件地址
    addrs = Address.objects.filter(user=user)

    # 组织上下文
    sku_ids = ','.join(sku_ids)  # [1,25]->1,25
    context = {'skus': skus,
               'total_count': total_count,
               'total_price': total_price,
               'transit_price': transit_price,
               'total_pay': total_pay,
               'addrs': addrs,
               'sku_ids': sku_ids}
    return render(request, 'place_order.html', context)




def payorder(request):
    return None