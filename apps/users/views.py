from django.shortcuts import render, HttpResponse, redirect
from django.views.generic.base import View
from .myform import RegisterForm, LoginForm, UserInfoForm, ModifyPwdForm  # 对外隐藏
from django.http import JsonResponse, HttpResponseRedirect
import json
from users.models import Userlog
from movie import models
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter  # Image用来生成图片，ImageDraw在图片上写字，ImageFont字体样式
from io import BytesIO, StringIO  # 能帮你保存数据，并且在取的时候会以二进制的形式返回给你
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from geetest import GeetestLib
from utils.mixin_utils import LoginRequireMixin
from django.conf import settings

from django.apps import AppConfig  # 导入百度AI
from aip.face import AipFace  # 导入百度人脸接口
import urllib
from django.db import transaction  # django内置事务
import base64
from django.core.urlresolvers import reverse
from pure_pagination import PageNotAnInteger, Paginator
from datetime import datetime



# from jyapp.ErrorCode import *  # 官网给出的状态码，通过pandas读出保存到。。。。


# 百度AI基本信息,公钥私钥，实例化
class AppConfig(AppConfig):
    # name = 'wpr'
    client = AipFace(settings.APP_ID, settings.API_KEY, settings.SECRECT_KEY)  # 实例化的对象，用它对数据进行加密并生成URl
    '''
    使用HttpClient，一般都需要设置连接超时时间和获取数据超时时间。
    这两个参数很重要，目的是为了防止访问其他http时，由于超时导致自己的应用受影响。
    '''
    # 说明：人脸注册完毕后，生效时间一般为5s以内，之后便可以进行识别或认证操作。
    # 设置建立连接的超时时间5s
    client.setConnectionTimeoutInMillis(1000 * 5)
    # 表示的是等待服务端响应数据的超时时间5s,通过打开的连接传输数据的超时时间
    client.setSocketTimeoutInMillis(1000 * 5)



# 注册(调用百度AI进行注册)
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()  # 实例化form对象
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        """
            :param :image;imageType;groupId;userId;可选参数options
            :return:face_token(人脸图片的唯一标识)；log_id(请求标识码，随机数);location(人脸在图片中的位置)

            逻辑：
                前台拿到图片的base64编码字符串，赋值给image上传给百度云端的用户组中，以便后续进行登录比较；
                再将人脸图片存入数据库中
                定义参数；
                带参数调用人脸注册接口addUser
            """
        back_dic = {'code': 100, 'msg': ''}
        register_form = RegisterForm(request.POST)
        username = request.POST.get('username')
        image = request.POST.get('imagecontent')  # 获得图片的base64编码，目的是快速传输
        gender = request.POST.get('gender')

        if register_form.is_valid():
            data = register_form.cleaned_data
            data.pop('confirm_password')  # 不把多余字段存进数据库中
            data['gender'] = gender

            # 引入事务，存数据库和存云端要么同时成功，要么同时失败
            try:
                with transaction.atomic():
                    # 对base64图片进行解码，解码后可以写入本地文件夹中或者数据库中，如果直接存会因为编码太大而不能存
                    base64_decode = base64.b64decode(image)
                    with open('static/faceregisterpic/' + username + '.jpeg', 'wb') as f:
                        f.write(base64_decode)
                    # models.UserProfile.objects.create(imagecontent='static/faceregisterpic/' + username + '.jpeg')
                    # data['imagecontent']
                    # print(data)
                    # 数据库中存入用户信息
                    # 这里不存数据库了，因为云端和本地文件都有了，减轻数据库的压力，就算存进去也是存的静态路径
                    # models.UserProfile.objects.create_user(**data,imagecontent='static/faceregisterpic/' + username + '.jpeg')
                    models.UserProfile.objects.create_user(**data)

                    if not image:
                        back_dic['code'] = 101
                        back_dic['msg'] = '获取图片有误'
                        return JsonResponse
                    # 组和编码是固定的
                    imageType = 'BASE64'
                    groupId = "register"
                    phone = request.POST.get('phone')
                    # 上传到云端的用户用用户名和电话作为名字
                    userId = username + phone

                    """可选参数"""
                    options = {}
                    options["user_info"] = "user's info"
                    options["quality_control"] = "NORMAL"
                    options["liveness_control"] = "LOW"
                    options["action_type"] = "REPLACE"

                    """ 调用人脸注册api """
                    res = AppConfig.client.addUser(image, imageType, groupId, userId, options)
                    print(res)
                    # print(res.get('error_msg'))
                    back_dic['url'] = '/login/'
                    # 如果图片有问题，参照不同的code代表不同的msg
                    # back_dic['code']=res.get('error_code')
                    # back_dic['msg'] = res.get('error_msg')
                    # back_dic['msg'] = res.error_msg  # 如果超时或者在上传的过程中出错，则返回出错信息
                    return JsonResponse(back_dic)
            except:
                back_dic['msg'] = '注册失败'
                return JsonResponse(back_dic)
        back_dic['code'] = 101
        back_dic['msg'] = register_form.errors
        return JsonResponse(back_dic)


# 判断性别
def gender(request):
    back_dic = {"code": 100, "msg": ''}
    if request.is_ajax():
        is_female = request.POST.get('is_Female')  # 如果选择的是男生则is_female为false
        # is_female = json.loads(is_female)  # 利用json模块反序列成后端python布尔值类型
        # user_id = request.POST.get('')
        # print(is_female)
        # user_id =request.POST.get('user_id')
        # print(user_id)
        if not is_female:  # 如果不是女生(true)
            back_dic['code'] = 101
    return JsonResponse(back_dic)


# 随机生成RGB参数
def get_random():
    return random.randint(128, 255), random.randint(128, 255), random.randint(128, 255)


# 获取验证码
def get_code(request):
    img_obj = Image.new('RGB', (310, 35), get_random())
    # 生成一个画笔对象
    img_draw = ImageDraw.Draw(img_obj)
    # 生成一个字体对象
    img_font = ImageFont.truetype('static/fonts/myfont.ttf', 35)
    # 随机验证码：数字+小写字母+大写字母
    code = ''  # 定义一个字符串存储最终验证码
    for i in range(5):
        random_int = str(random.randint(0, 9))
        random_lower = chr(random.randint(97, 122))  # 小写字母范围是97——122
        random_upper = chr(random.randint(65, 90))  # 大写字母是65——90
        temp_code = random.choice([random_int, random_lower, random_upper])
        # 将产生的字一个一个写到图片上
        img_draw.text((60 + i * 45, 0), temp_code, get_random(), img_font)
        # code记录
        code += temp_code
    print(code)  # 后台打印验证码
    # 将code存放到session表中
    request.session['code'] = code
    # 生成io对象
    io_obj = BytesIO()
    img_obj.save(io_obj, 'png')
    return HttpResponse(io_obj.getvalue())


# 登录
class LoginView(View):
    def get(self, request):
        """
        先实例化form对象，可能一开始不校验，但是后续只需要将request字典传入即可;
        因为是get请求，直接跳转到登录界面
        :param request:
        :return:
        """
        login_form = LoginForm()
        return render(request, 'login.html', locals())

    def post(self, request):
        back_dic = {'code': 100, 'msg': ''}
        code = request.POST.get('code')
        # 先校验验证码，减轻数据库压力
        if request.session.get('code').lower() == code.lower():
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # 从客户端拿数据
                username = request.POST.get('username')  # 从正确数据中获得用户名
                # request.POST.get('username')  # 或者从request.POST中获得姓名
                password = request.POST.get('password')
                # 丢进auth的登录组件生成用户对象
                user_obj = auth.authenticate(username=username, password=password)
                if user_obj:
                    # 登录成功就记录当前登录状态
                    auth.login(request, user_obj)
                    log = Userlog()
                    log.ip = request.META['REMOTE_ADDR']
                    log.user = request.user
                    log.add_time = datetime.utcnow()
                    log.save()
                    back_dic['msg'] = "登录成功"
                    back_dic['url'] = '/index/'
                else:
                    back_dic['code'] = 101
                    back_dic['msg'] = '用户名或密码错误'
            else:
                back_dic['code'] = 102
                back_dic['msg'] = login_form.errors
        else:
            back_dic['code'] = 102
            back_dic['msg'] = "验证码错误"
        return JsonResponse(back_dic)


# 用极验滑动验证码登录
pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"


# 极验获取验证码
def get_slidecode(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


# 用极验验证码登录
class SlideLoginView(View):
    def get(self, request):
        """
        先实例化form对象，可能一开始不校验，但是后续只需要将request字典传入即可;
        因为是get请求，直接跳转到登录界面
        :param request:
        :return:
        """
        login_form = LoginForm()
        return render(request, 'slide_login.html', locals())

    def post(self, request):
        back_dic = {'code': 100, 'msg': ''}
        # 从客户端拿数据
        username = request.POST.get('username')  # 从正确数据中获得用户名
        # request.POST.get('username')  # 或者从request.POST中获得姓名
        password = request.POST.get('password')
        # 获取极验滑动验证码相关的参数
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)

        if result:
            user_obj = auth.authenticate(username=username, password=password)
            if user_obj:
                # 登录成功就记录当前登录状态
                auth.login(request, user_obj)
                log = Userlog()
                log.ip = request.META['REMOTE_ADDR']
                log.user = request.user
                log.add_time = datetime.utcnow()
                log.save()
                back_dic['msg'] = "登录成功"
                back_dic['url'] = '/index/'
            else:
                back_dic['code'] = 101
                back_dic['msg'] = "用户名或密码错误"
        else:
            back_dic['code'] = 102
            back_dic['msg'] = "验证码错误"
        return JsonResponse(back_dic)


# 调用百度AI人脸识别接口进行登录
class FaceLoginView(View):
    def get(self, request):
        return render(request, 'face_login.html')

    def post(self, request):
        """
        调用百度云的人脸搜索search接口进行登录
        :param request:image，image_type,group_id_list(从指定的group中进行查找 用逗号分隔，上限20个)
        :return: face_token,user_list(group_id,user_id,user_info,score[用户的匹配得分])
        """
        back_dic = {'code': 100, 'msg': ''}
        imagecontent = request.POST.get('imagecontent')
        image = imagecontent.split(',')[1]
        imageType = "BASE64"
        groupIdList = "register,wpr1"
        """可选参数"""
        options = {}
        options["max_face_num"] = 3
        options["match_threshold"] = 70
        options["quality_control"] = "NORMAL"
        options["liveness_control"] = "LOW"
        # options["user_id"] = "wpr1115151979063"  # 当需要对特定用户进行比对时，指定user_id进行比对。即人脸认证功能。
        # options["max_user_num"] = 3
        """调用人脸搜索"""
        res = AppConfig.client.search(image, imageType, groupIdList, options)
        # {'error_code': 0, 'error_msg': 'SUCCESS', 'log_id': 1345050745466482551, 'timestamp': 1564546648, 'cached': 0, 'result': {'face_token': '976e3c07416616cb598c9759580d075a', 'user_list': [{'group_id': 'register', 'user_id': 'baobao12345678901', 'user_info': "user's info", 'score': 97.097213745117}]}}
        print(res)
        user_id = res['result']['user_list'][0]['user_id']
        username = user_id[:-11]  # TODO:这个username怎么让index中查询的时候获取到
        # log_id = res['log_id']

        """调用身份验证(身份证必填)"""
        # idCardNumber = user_id # 用log_id作为idcard
        # vres = AppConfig.client.personVerify(image, imageType, idCardNumber, name)
        # print(vres)

        # obj = models.UserProfile.objects.filter(username=username).first()
        # password = obj.password
        # print(obj.password)

        # 丢进auth的登录组件生成用户对象(不可行)
        user_obj = auth.authenticate(username=username, password='123')

        # 取出分数
        score = res['result']['user_list'][0]['score']
        # print(score)
        if score >= 80:
            # 登录成功就记录当前登录状态
            auth.login(request, user_obj)
            log = Userlog()
            log.ip = request.META['REMOTE_ADDR']
            log.user = request.user
            log.add_time = datetime.utcnow()
            log.save()
            back_dic['url'] = '/index/'
        else:
            back_dic['code'] = 101
            back_dic['msg'] = "登录失败"
        return JsonResponse(back_dic)


# 主页
class IndexView(View):
    '''
    主页没有提交数据，所以只用到get请求；
    主页要用到的数据：
        电影表中——海报、电影名、评分、播放量、评论数、上映时间、时长、标签
        用户评论表——评论内容
    难点：
        1、在评论数中显示热评，截取一定长度的评论内容，然后剩余的部分用>>>完整热评收起来，点击后就会在下面显示
        2、播放量和评论数只显示六个
    '''

    def get(self, request):
        tag_id = request.GET.get('tag_id', 1)  # 默认为1
        movies = models.Movie.objects.filter(tag=tag_id).all()
        # 根据movie_id来查询出movies
        # print(movies)
        tags = models.Tag.objects.all()
        comments = models.Comment.objects.all()
        # 从数据库中查，按照上映时间进行排序，取6个，渲染到页面上
        movie_time = models.Movie.objects.order_by('-release_time')[:6]
        # 按照播放量进行排序，取6个
        movie_playnums = models.Movie.objects.order_by('-play_nums')[:6]
        # 按照评论数排序
        movie_commentnums = models.Movie.objects.order_by('-comment_nums')[:6]
        # 按照评分排序
        movie_mark = models.Movie.objects.filter(star__gt=9).order_by('-star')[:6]

        # 当登录方式为人脸登录的时候，查询出用户名
        # user_obj = models.UserProfile.objects.filter(username=name).first()

        return render(request, 'index.html',
                      {'movies': movies, 'tags': tags, 'tag_id': tag_id, 'comments': comments,
                       'movie_time': movie_time, 'movie_playnums': movie_playnums,
                       'movie_commentnums': movie_commentnums, 'movie_mark': movie_mark})


# , 'user_obj': user_obj

# 注销
def logout(request):
    auth.logout(request)
    return redirect('/index/')


# 个人中心
class UserInfoView(LoginRequireMixin, View):
    '''
    这里继承的是登录访问权限，对访问进行权限设置；
    不登录就不能登录到个人中心，未登录会自动跳转到登录页面;
    先对字段进行校验；
    校验通过就将信息保存，重新定位到当前页面
    '''

    def get(self, request):
        # form_obj = UserInfoForm()
        return render(request, 'userinfo.html')

    def post(self, request):
        userinfo_form = UserInfoForm(request.POST, request.FILES, instance=request.user)
        if userinfo_form.is_valid():
            userinfo_form.save()
            return HttpResponseRedirect(reverse("users:userinfo"))
        else:
            # 通过json的dumps方法把字典转换为json字符串
            return HttpResponse(json.dumps(userinfo_form.errors), content_type='application/json')



# 修改密码
class ForgetView(LoginRequireMixin, View):
    def get(self, request):
        modify_form = ModifyPwdForm()
        return render(request, 'forgetpwd.html', locals())

    def post(self, request):
        back_dic = {'code': 100, 'msg': ''}
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            confirm_password = request.POST.get('confirm_password')

            user = request.user
            # 加密成密文
            user.password = make_password(confirm_password)
            print(user.password)
            user.save()
            # 修改成功跳转到登录界面
            back_dic['url'] = '/login/'
        else:
            back_dic['code'] = 404
            back_dic['msg'] = modify_form.errors
        return JsonResponse(back_dic)


# 评论记录
class CommentListView(LoginRequireMixin, View):
    def get(self, request):
        comments = models.Comment.objects.filter(user=request.user)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(comments, 3, request=request)
        comments = p.page(page)
        return render(request, 'comments.html', {'comments': comments})


# 登录日志
class LoginLogView(LoginRequireMixin, View):
    def get(self, request):
        logs = Userlog.objects.filter(user=request.user)
        return render(request, 'loginlog.html', {"logs": logs})


# 个人中心的收藏电影
class FavMovieView(LoginRequireMixin, View):
    def get(self, request):
        fav_movies = models.Moviecol.objects.filter(user=request.user)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(fav_movies, 4, request=request)
        fav_movies = p.page(page)
        return render(request, 'moviecol.html', {'fav_movies': fav_movies})
