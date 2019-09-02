from django.db import models

# Create your models here.

from django.db import models

from django.contrib.auth.models import AbstractUser
from datetime import datetime
import uuid

'''
关于class Meta
    通过一个内嵌类 "class Meta" 给你的 model 定义元数据/
    class Meta做为嵌套类，主要目的是给上级类添加一些功能，或者指定一些标准。
    
    verbose_name的意思很简单，就是给你的模型类起一个更可读的名字：class MainWheel(Main):
        若未提供该选项, Django 则会用一个类名字的 munged 版本来代替: CamelCase becomes camel case
    verbose_name_plural：这个选项是指定，模型的复数形式是什么
    
    此外还有别的用法：https://www.cnblogs.com/tongchengbin/p/7670927.html
    
    ----常用----
    # 轮播banner
    class Meta:
        db_table = 'axf_wheel'
        
关于def __unicode__(self)和 def __str__(self):  
    py3中用的是__str__
    py2中用的是__unicode__  因为更安全一些 
'''


# 用户信息表
'''
verbose_name是指该字段展示出来的名字:
    self.model_class._meta.get_field(field_name).verbose_name   
    在_meta中有个get_field方法,通过将model字段名称传入进去，最后执行.verbose_name就可以获取model字段名称
upload_to涉及到文件上传的路径;
choice用于作出选择；
blank就是先空着，字段的其他属性还是继承着；null指可以不写
'''


class UserProfile(AbstractUser):
    name = models.CharField(verbose_name='昵称', max_length=64, default='')
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    gender = models.CharField(verbose_name='性别', max_length=8, choices=(("male", "男"), ("female", "女")),
                              default='female')
    info = models.CharField(verbose_name='个人简介', default='', max_length=255)
    image = models.ImageField(verbose_name='头像', max_length=100, upload_to='image/%Y/%m', default='image/default.png')
    phone = models.CharField(verbose_name='手机号码', max_length=11, null=True, blank=True)
    add_time = models.DateField(verbose_name='添加时间', default=datetime.now)
    # 用户人脸注册的人脸图像，该字段会将接收到的文件自动存放到faceimg文件夹下，只存该文件的路径，比如：faceimg/111.png
    imagecontent = models.FileField(upload_to='faceimg/',default='')
    '''
    Python使用UUID库生成唯一ID
    UUID是128位的全局唯一标识符，通常由32字节的字符串表示。它可以保证时间和空间的唯一性，也称为GUID，全称为：UUID —— Universally Unique IDentifier，Python 中叫 UUID。
    它通过MAC地址、时间戳、命名空间、随机数、伪随机数来保证生成ID的唯一性。
    UUID主要有五个算法，也就是五种方法来实现。
    
    uuid1()——基于时间戳。由MAC地址、当前时间戳、随机数生成。可以保证全球范围内的唯一性，但MAC的使用同时带来安全性问题，局域网中可以使用IP来代替MAC。
    uuid2()——基于分布式计算环境DCE（Python中没有这个函数）。算法与uuid1相同，不同的是把时间戳的前4位置换为POSIX的UID。实际中很少用到该方法。
    uuid3()——基于名字的MD5散列值。通过计算名字和命名空间的MD5散列值得到，保证了同一命名空间中不同名字的唯一性，和不同命名空间的唯一性，但同一命名空间的同一名字生成相同的uuid。
    uuid4()——基于随机数。由伪随机数得到，有一定的重复概率，该概率可以计算出来。
    uuid5()——基于名字的SHA-1散列值。算法与uuid3相同，不同的是使用 Secure Hash Algorithm 1 算法。
    '''
    uuid = models.CharField(verbose_name='唯一标识符', max_length=50, default=uuid.uuid4())

    # 内嵌元类，给上一层类增加增加功能，比如让这张用户表的总名称叫用户信息表(也可以说成模型的复数形式)，里面有很多冗长的名字
    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name  # plural表示复数

    # def __unicode__(self):
    #     return self.username  # 返回的是用户名
    def __str__(self):
        return self.username  # 返回auth组件中的用户名


# 用户日志表
'''
on_delete是外键的删除
1、常见的使用方式(设置为null) >>> on_delete=models.SET_NULL
2、关于别的属性的介绍
    CASCADE:这就是默认的选项，级联删除，你无需显性指定它。
    PROTECT: 保护模式，如果采用该选项，删除的时候，会抛出ProtectedError错误。
    SET_NULL: 置空模式，删除的时候，外键字段被设置为空，前提就是blank=True, null=True,定义该字段的时候，允许为空。
    SET_DEFAULT: 置默认值，删除的时候，外键字段设置为默认值，所以定义外键的时候注意加上一个默认值。
    SET(): 自定义一个值，该值当然只能是对应的实体了
3、补充说明:关于SET()的使用
**官方案例**
def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class MyModel(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
    )
'''


class Userlog(models.Model):
    ip = models.CharField(verbose_name='登录ip', max_length=64, default='')
    add_time = models.DateField(verbose_name='登录时间', default=datetime.now)
    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE, default='')

    class Meta:
        verbose_name = "登录日志"
        verbose_name_plural = verbose_name

    # def __unicode__(self):
    #     return self.user  # 返回的是外键字段中的用户名

    def __str__(self):
        return self.user

