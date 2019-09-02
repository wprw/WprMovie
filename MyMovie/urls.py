"""MyMovie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# from django.contrib import admin
import xadmin
from django.views.static import serve
from users.views import RegisterView, IndexView, FaceLoginView
from movie.views import MoviePlayView, MovieTagView, SearchView, MovieReleasetimeView, MoviePlaynumsView, MovieMarkView, \
    MovieCommentView
from users import views as users_view
from movie import views as movie_view
from MyMovie import settings
from rest_framework.documentation import include_docs_urls

'''
as_view()调用函数,会根据请求方式,返回对应的函数名；

'''
urlpatterns = [
    # 普通django后台管理
    # url(r'^admin/', admin.site.urls),

    # 超级后台
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view()),
    # 主页
    url(r'^index/', IndexView.as_view(), name='index'),
    # 电影标签分类接口
    url(r'^movietag/$', MovieTagView.as_view(), name='movietag'),
    # 评分分类接口
    url(r'^moviemark/$', MovieMarkView.as_view(), name='moviemark'),
    # 上映时间分类接口
    url(r'^moviereleasetime/$', MovieReleasetimeView.as_view(), name='moviereleasetime'),
    # 播放量分类接口
    url(r'^movieplaynums/$', MoviePlaynumsView.as_view(), name='movieplaynums'),
    # 评论数分类接口
    url(r'^moviecomments/$', MovieCommentView.as_view(), name='moviecomments'),

    # 注册
    url(r'^register/$', RegisterView.as_view(), name='register'),

    # 人脸注册
    # url(r'^faceregister/$', FaceRegisterView.as_view(), name='faceregister'),

    # 判断性别
    url(r'^gender/', users_view.gender, name='gender'),

    # 获取验证码(极验滑动验证码)
    url(r'^pc-geetest/register/', users_view.get_slidecode, name='get_slidecode'),
    # 极验滑动验证码登录
    url(r'^slide_login/', users_view.SlideLoginView.as_view(), name='slide_login'),
    url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),  # 配置media文件夹

    # 人脸登录
    url(r'face_login/', FaceLoginView.as_view(), name='face_login'),

    # 获取验证码(手动)
    url(r'^get_code/', users_view.get_code, name='get_code'),
    # 图片验证码登录
    url(r'login/$', users_view.LoginView.as_view(), name='login'),

    # 注销
    url(r'^logout/$', users_view.logout, name='logout'),

    # 搜索
    url(r'^search/$', SearchView.as_view(), name='search'),

    # 播放电影
    url(r'^play/(?P<movie_id>.*)/$', MoviePlayView.as_view(), name='play'),

    # 用户评论
    url(r'^comment/$', movie_view.comment, name='comment'),
    # 影评
    url(r'^filmreview/$', movie_view.film_review, name='filmreview'),

    # 收藏电影
    url(r'^colmovie/$', movie_view.colmovie, name='colmovie'),

    # 个人中心
    url(r'^users/', include('users.urls', namespace='users')),
    # url(r'^userinfo/', UserInfoView.as_view(), name='userinfo'),

    # 接口文档
    url(r'^docs/', include_docs_urls(title='时光网的文档')),

]
