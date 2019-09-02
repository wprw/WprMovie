from django.conf.urls import url
from users.views import UserInfoView, ForgetView, CommentListView, LoginLogView, FavMovieView

urlpatterns = [
    # 个人中心
    url(r'^userinfo/$', UserInfoView.as_view(), name='userinfo'),
    # 修改密码
    url('forget/pwd/', ForgetView.as_view(), name='forget_pwd'),
    # 评论记录
    url(r'^comment/$', CommentListView.as_view(), name='comment'),
    # 登录日志
    url(r'^log/$', LoginLogView.as_view(), name='login_log'),
    # 收藏电影
    url(r'^fav_movie/$', FavMovieView.as_view(), name='fav_movie')
]
