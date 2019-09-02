from django.shortcuts import render, HttpResponse
from django.views.generic.base import View
from movie import models
from pure_pagination import Paginator, PageNotAnInteger
from movie import movieform
from django.db import transaction
from django.db.models import F, Q
from django.http import JsonResponse
from rest_framework.response import Response
# 电影分类
# 电影
from rest_framework.generics import ListAPIView
# 过滤字段
from django_filters.rest_framework.backends import DjangoFilterBackend
# 排序过滤字段
# from rest_framework.filters import OrderingFilter
from movie import serializers


# 根据分类查找出对应电影的接口
class MovieTagView(ListAPIView):
    # authentication_classes = []  # auth认证局部禁用
    queryset = models.Movie.objects
    serializer_class = serializers.MovieModelSerializer
    filter_backends = [DjangoFilterBackend]
    # 根据tag分类来过滤
    filter_fields = ['tag']


# 根据评分分类接口
class MovieMarkView(ListAPIView):
    # authentication_classes = []  # auth认证局部禁用

    def get(self, request, *args, **kwargs):
        star = request.query_params.get('star', '9')
        superstar = float(star) + 0.99
        movie_mark = models.Movie.objects.filter(Q(star__gte=star) & Q(star__lt=superstar)).order_by('-star')[:6]
        res = serializers.MovieModelSerializer(movie_mark, many=True).data
        return Response({
            'data': res
        })


# 根据上映时间查找出对应电影的接口
class MovieReleasetimeView(ListAPIView):
    """
    queryset = models.Movie.objects
    # print(queryset)
    serializer_class = serializers.MovieModelSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # 根据评分来过滤
    # filter_fields = ['star']
    # 对ordering过滤字段进行排序
    ordering_fields = ['release_time', 'play_nums', 'comment_nums']

    def get(self, request, *args, **kwargs):
        # time_tag = request.query_params.get('time_tag')  # get请求数据都在request.query_params，post请求数据都在request.data中
        response = super().get(request, *args, **kwargs)
        # if time_tag == '1':
        #     response.data = response.data[:6]
        # else:
        #     response.data = response.data[6:12]
        response.data = response.data[:6]
        return response
    """
    # authentication_classes = []  # auth认证局部禁用

    def get(self, request, *args, **kwargs):
        # 从前台获得请求数据  http://127.0.0.1:8888/moviereleasetime/?ordering=play_nums
        ordering = request.query_params.get('ordering', 'id')
        # 从数据库中查出数据进行排序处理
        movie_list = models.Movie.objects.order_by(ordering)[:6]
        # 返回给前台结果
        return Response({
            'data': serializers.MovieModelSerializer(movie_list, many=True).data
        })


# 根据播放量查找出对应电影的接口
class MoviePlaynumsView(ListAPIView):
    # authentication_classes = []  # auth认证局部禁用

    def get(self, request, *args, **kwargs):
        # 从前台获取请求数据
        play_nums = request.query_params.get('ordering', 'id')  # 从get请求中获取numordering，没有的话默认按id排序
        # 从数据库中查出数据进行排序处理 http://127.0.0.1:8888/movieplaynums/?ordering=-play_nums
        movienums_list = models.Movie.objects.order_by(play_nums)[:6]
        # 返回给前台结果
        res = serializers.MovieModelSerializer(movienums_list, many=True).data
        return Response({'data': res})


# 根据评论数查找出对应电影的接口
class MovieCommentView(ListAPIView):
    # authentication_classes = []  # auth认证局部禁用

    def get(self, request, *args, **kwargs):
        comment_nums = request.query_params.get('ordering', 'id')
        # http://127.0.0.1:8888/moviecomments/?ordering=-comment_nums
        comments_list = models.Movie.objects.order_by(comment_nums)[:6]
        res = serializers.MovieModelSerializer(comments_list, many=True).data
        return Response({'data': res})


# 搜索
class SearchView(View):
    def get(self, request):
        # 从前台获取搜索关键字
        search_keywords = request.GET.get('keywords')
        if search_keywords:
            # 从数据库中进行模糊查询
            movies = models.Movie.objects.filter(Q(
                title__icontains=search_keywords))
            # 统计查询出的个数
            counts = movies.count()
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 1
            p = Paginator(movies, 5, request=request)
            movies = p.page(page)
            return render(request, 'search.html',
                          {'movies': movies, 'search_keywords': search_keywords, 'counts': counts})
        return HttpResponse('暂时没有你要找的电影，可以联系管理员问他要！！')


# 播放电影 (未登录则不能看电影，跳转到登录界面)

class MoviePlayView(View):
    def get(self, request, movie_id):
        movie = models.Movie.objects.get(id=movie_id)
        comments = models.Comment.objects.filter(movie_id=movie_id).order_by('-add_time')  # 按添加时间的倒序排列,找到最新的评论
        # 判断用户是否登录
        if request.user.is_authenticated():
            col_movie = models.Moviecol.objects.filter(user=request.user, movie_id=movie_id).first()
            models.Movie.objects.filter(id=movie_id).update(play_nums=F('play_nums') + 1)

            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:  # 如果是无效页面，则返回第一页
                page = 1
            p = Paginator(comments, 8, request=request)  # 设置每一页显示几条
            comments = p.page(page)
            return render(request, 'play.html', {"movie": movie, "comments": comments, 'col_movie': col_movie})
        else:
            try:
                page = request.GET.get('page', 1)
            except PageNotAnInteger:  # 如果是无效页面，则返回第一页
                page = 1
            p = Paginator(comments, 5, request=request)  # 设置每一页显示几条
            comments = p.page(page)
            return render(request, 'playnoauth.html', {"movie": movie, "comments": comments})




# 评论
def comment(request):

    if request.method == 'POST':
        back_dic = {'code': 100, 'msg': ''}
        # 没有登录的情况就转到登录界面
        if not request.user.is_authenticated():
            return render(request, 'login.html')
        # 登录之后先校验评论内容
        comment_form = movieform.CommentForm(request.POST)
        # 如果校验通过，则从前台获取数据，后端从数据库获取数据，两者进行比较
        if comment_form.is_valid():
            with transaction.atomic():
                content = request.POST.get('content')
                movie_id = request.POST.get('movie_id')
                # 将数据存到评论表中
                models.Comment.objects.create(user=request.user, content=content, movie_id=movie_id)
                # 电影表中的评论数字段+1
                models.Movie.objects.filter(id=movie_id).update(comment_nums=F('comment_nums') + 1)
                back_dic['msg'] = "评论成功"
            return JsonResponse(back_dic)
        else:
            back_dic['code'] = 101
            print(comment_form.errors)
            back_dic['msg'] = comment_form.errors
            return JsonResponse(back_dic)


# 添加收藏
def colmovie(request):
    if request.method == 'POST':
        back_dic = {'code': 100, 'msg': ''}
        movie_id = request.POST.get('movie_id')
        models.Moviecol.objects.create(user=request.user, movie_id=movie_id)
        back_dic['msg'] = "收藏成功"
        return JsonResponse(back_dic)





# 影评
def film_review(request):
    movie_obj = models.Movie.objects.all()
    user_obj = models.UserProfile.objects.all()
    comment_obj = models.Comment.objects.all()
    return render(request, 'film_review.html',
                  {'movie_obj': movie_obj, 'user_obj': user_obj, 'comment_obj': comment_obj})
