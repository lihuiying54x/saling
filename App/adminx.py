import xadmin
from xadmin import views
from .models import User,GoodsType,Goods,GoodsSKU,IndexTypeGoodsBanner,IndexPromotionBanner,IndexGoodsBanner,OrderGoods,OrderInfo,Address
from xadmin.views import BaseAdminView
class GoodsAdmin(object):
    style_fields = {"detail":"ueditor"}

class ThemeAdmin(object):
    enable_themes = True
    use_bootswatch = True
xadmin.site.register(BaseAdminView,ThemeAdmin)

class GlobalSetting(object):
    site_title = '生鲜网管理'
    site_footer = '生鲜网'
    menu_style = 'accordion'
xadmin.site.register(views.CommAdminView,GlobalSetting)

class UserSetting(object):
    list_display = ('uname','uemail')

class UserAdmin(object):
    list_display=['uname','uemail']
    search_fields=['uname']
    model_icon='fa fa-user'

class GoodsSKUAdmin(object):
    model_icon = 'fa fa-gift'

class OrderInfoAdmin(object):
    data_charts = {
        "order_amount":{'title':'订单金额',"x-field":"create_time","y-field":('total_price',),"order": ('create_time',)},
        "order_count":{'title':'订单量',"x-field":"create_time","y-field": ('total_count',),"order": ('create_time',)},
    }

xadmin.site.register(User,UserAdmin)
xadmin.site.register(GoodsType)
xadmin.site.register(GoodsSKU,GoodsSKUAdmin)
xadmin.site.register(Goods,GoodsAdmin)
xadmin.site.register(IndexGoodsBanner)
xadmin.site.register(IndexPromotionBanner)
xadmin.site.register(IndexTypeGoodsBanner)
xadmin.site.register(OrderInfo,OrderInfoAdmin)
xadmin.site.register(OrderGoods)
xadmin.site.register(Address)