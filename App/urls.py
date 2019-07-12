from django.conf.urls import url

from App import views


urlpatterns = [
    url(r'^register/$',views.register ),
    url(r'^register_handle/$',views.register_handle,name='register_handle'),
    url(r"^index/$",views.index,name='index'),
    # url(r"^index/$",views.index,name='index'),
    url(r'^register_exist/$', views.register_exist),
    url(r'^login/$', views.login,name='login'),
    url(r'^login_handle/$', views.login_handle,name='login_handle'),
    url(r'^info/$', views.info,name='info'),
    url(r'^order/$', views.order,name='order'),
    url(r'^site/$', views.site,name='site'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^getcode/$',views.getCode,name='getcode'),
    # url(r'^login1/$',views.login1,name='login1'),
    url(r'^sms/$',views.sms,name='sms'),
    url(r'list/(?P<type>\d+)/(?P<page_num>\d+)/$', views.list, name='list'),
    url(r'^(\d+)/$', views.detail, name='detail'),     #详细页
    url(r'^search/$',views.MySearchView(),name='search'),

    url(r'^cart/$', views.cart, name='cart'),
    url(r'^add/$',views.add, name='add'),
    url(r'^update/$',views.update, name='update'),
    url(r'^delete/$',views.delete, name='delete'),

    # # url(r'^add(\d+)_(\d+)/$', views.add),  # 加入购物车  分别为商品的id和数量
    # url(r'^add(\d+)_(\d+)/$', views.add),  # 加入购物车  分别为商品的id和数量
    # url(r'^edit(\d+)_(\d+)/$', views.edit),  # 修改购物车中商品的数量 分别为商品的id和数量
    # url(r'^delete(\d+)/$', views.delete),  # 删除购物车中的某个商品
    url(r'^place_order/$', views.place_order,name='place'),
    # url(r'^change/$',views.change,name='change'),
    url(r'^payorder/$',views.payorder,name='payorder')



]