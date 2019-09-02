import xadmin

from users import models
from xadmin import views

# 报错 The model UserProfile is already registered
# 先注销，再注册
xadmin.site.unregister(models.UserProfile)
xadmin.site.register(models.UserProfile)

xadmin.site.register(models.Userlog)


# 自定义Xadmin样式
class GlobalSettings(object):
    site_title = "万佩佩的超级后台"
    site_footer = "若有疑问请联系站长 @ 万佩佩"
    menu_style = 'accordion'  # 左边导航栏 收缩 手风琴


xadmin.site.register(views.CommAdminView, GlobalSettings)
