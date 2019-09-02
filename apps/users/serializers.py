'''
序列化就是接口给前台提供哪些数据字段;
序列化涉及到外键的时候最好从小到大，从上往下写序列化
'''
from rest_framework.serializers import ModelSerializer
from users import models


# 标签的序列化
class UserProfileModelSerializer(ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ['id', 'name']
