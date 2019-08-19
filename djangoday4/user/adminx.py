import xadmin
from article.models import Article, Tag
from user.models import UserProfile

# xadmin.site.register(UserProfile)
from xadmin import views


class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = '博客后台管理'
    site_footer = '达达的博客公司'

# 注册
xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, GlobalSettings)
