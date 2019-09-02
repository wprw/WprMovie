from django.db import models
from datetime import datetime
from users.models import UserProfile  # 🌈这里设计到两个应用中的模型表相关连，需要导入使用

# Create your models here.

'''
链接用CharField

DateTimeField的两个重要参数：（参数互斥，不能共存）
auto_now:每当对象被保存时将字段设为当前日期，常用于保存最后修改时间。
auto_now_add：每当对象被创建时，设为当前日期，常用于保存创建日期(注意，它是不可修改的)。
设置上面两个参数就相当于给field添加了editable=False和blank=True属性。
如果想具有修改属性，请用default参数。

一对多创建外键两种：
    1、movie = models.ForeignKey(to='Movie')
    2、movie = models.ForeignKey(Movie,verbose_name="相关电影")  ⚠️注意用这种方式创建外键，要先将Movie表创建出来写在上面

外键的级联删除，django2.x往上一定要加上,django2.x之前版本不加没事
on_delete=models.CASCADE
'''


# 标签
class Tag(models.Model):
    name = models.CharField(verbose_name="名称", max_length=128)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 电影信息
class Movie(models.Model):
    title = models.CharField(verbose_name="电影标题", max_length=255)
    info = models.TextField(verbose_name="电影简介", default='')
    # 按照年月将海报图片存放在banner文件夹下
    logo = models.ImageField(verbose_name="海报图片", max_length=255, upload_to='banner/%Y/%m', default='image/default.png')
    star = models.FloatField(verbose_name="推荐指数")
    play_nums = models.IntegerField(verbose_name="播放量")
    comment_nums = models.IntegerField(verbose_name="评论数")
    area = models.CharField(verbose_name="上映地区", max_length=255)
    release_time = models.DateField(verbose_name="上映时间", default=datetime.now)
    length = models.CharField(verbose_name="时长", max_length=255)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)
    download_url = models.CharField(verbose_name="下载链接", max_length=300, default='')
    # 该字段会将接收到的文件自动存放到videos文件夹下，只存该文件的路径，按照年月的文件夹来存，比如：videos/2019/06
    movie_file = models.FileField(verbose_name="电影文件", max_length=255, upload_to='videos/%Y/%m',
                                  default='videos/default.mp4')
    # 播放电影的唯一标识，表示是哪部电影
    play_id = models.CharField(verbose_name="电影ID", max_length=255, default='', blank=True)  # 设置blank表示后台中可以不写
    # 电影与分类是一对多的,on_delete=models.CASCADE是主外关系键中的级联删除，也就是当删除主表的数据时候，该外键也删除
    """
    on_delete参数的各个值的含义:
    on_delete=None,               # 删除关联表中的数据时,当前表与其关联的field的行为
    on_delete=models.CASCADE,     # 删除关联数据,与之关联也删除
    on_delete=models.DO_NOTHING,  # 删除关联数据,什么也不做
    on_delete=models.PROTECT,     # 删除关联数据,引发错误ProtectedError
    # models.ForeignKey('关联表', on_delete=models.SET_NULL, blank=True, null=True)
    on_delete=models.SET_NULL,    # 删除关联数据,与之关联的值设置为null（前提FK字段需要设置为可空,一对一同理）
    # models.ForeignKey('关联表', on_delete=models.SET_DEFAULT, default='默认值')
    on_delete=models.SET_DEFAULT, # 删除关联数据,与之关联的值设置为默认值（前提FK字段需要设置默认值,一对一同理）
    on_delete=models.SET,         # 删除关联数据,
        a. 与之关联的值设置为指定值,设置：models.SET(值)
        b. 与之关联的值设置为可执行对象的返回值,设置：models.SET(可执行对象)
    """
    # 用这种方法创建外键字段，需要将Tag先创建出来，也就是写在上面
    tag = models.ForeignKey(Tag, verbose_name="电影标签", on_delete=models.CASCADE, default='')

    # tag = models.ForeignKey(to='Tag', verbose_name="电影标签", on_delete=models.CASCADE, default='')

    class Meta:
        verbose_name = "电影信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


# 用户评论
class Comment(models.Model):
    content = models.TextField(verbose_name="评论内容", default='')
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    movie = models.ForeignKey(Movie, verbose_name="电影", on_delete=models.CASCADE)  # 电影与评论是一对多
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)  # 评论与用户是一对多  UserProfile是用户简介

    class Meta:
        verbose_name = "用户评论"
        verbose_name_plural = verbose_name


# 上映预告(主要是用来放在轮播图中的)
class Preview(models.Model):
    title = models.CharField(verbose_name="电影标题", max_length=255)
    logo = models.ImageField(verbose_name="海报图片", upload_to='banner/%Y/%m', default='image/default.png', max_length=128)
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "上映预告"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


# 用户收藏 col是collect的意思
class Moviecol(models.Model):
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)
    movie = models.ForeignKey(Movie, verbose_name="电影", on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, verbose_name="用户", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name
