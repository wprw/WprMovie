from django import forms
from django.forms import widgets
from users import models


# 对注册进行校验
class RegisterForm(forms.Form):
    username = forms.CharField(required=True, label='用户名', error_messages={'required': "用户名不为空", },
                               widget=widgets.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required=True, min_length=3, label='密码', max_length=8,
                               error_messages={'min_length': "密码最少3位", 'max_length': '密码最大8位', 'required': "密码不为空"},
                               widget=widgets.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(required=True, min_length=3, label='确认密码', max_length=8,
                                       error_messages={'min_length': "确认密码最少3位", 'max_length': '确认密码最大8位',
                                                       'required': "确认密码不为空"},
                                       widget=widgets.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, label='邮箱', error_messages={'required': "邮箱不为空", 'invalid': "邮箱不合法"},
                             widget=widgets.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(required=True, label='电话号码', error_messages={'required': "手机号码不为空"},
                            widget=widgets.TextInput(attrs={'class': 'form-control'}))

    # 对确认密码增加全局钩子函数
    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if not password == confirm_password:
            self.add_error('confirm_password', "两次输入密码不一致")
        return self.cleaned_data

    # 对手机号码进行二次校验
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) != 11:
            self.add_error('phone', "密码长度必须为11位")
        return phone

    # 对用户名进行是否重复校验
    def clean_username(self):
        username = self.cleaned_data.get('username')
        namedate = models.UserProfile.objects.filter(username=username)
        if namedate:
            self.add_error('username', '用户名已存在')
        return username


# 登录校验
class LoginForm(forms.Form):
    username = forms.CharField(required=True, label='用户名', error_messages={'required': "用户名不为空", },
                               widget=widgets.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required=True, min_length=3, label='密码', max_length=8,
                               error_messages={'min_length': "密码最少3位", 'max_length': '密码最大8位', 'required': "密码不为空"},
                               widget=widgets.PasswordInput(attrs={'class': 'form-control'}))


# 个人中心修改个人信息校验
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = ['name', 'email', 'phone', 'image', 'info']


# 个人中心修改密码校验
class ModifyPwdForm(forms.Form):
    new_password = forms.CharField(required=True, min_length=3, max_length=8,
                                   error_messages={'min_length': "密码最少3位", 'max_length': '密码最大8位', 'required': "密码不为空"},
                                   widget=widgets.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(required=True, min_length=3, max_length=8,
                                       error_messages={'min_length': "密码最少3位", 'max_length': '密码最大8位',
                                                       'required': "密码不为空"},
                                       widget=widgets.PasswordInput(attrs={'class': 'form-control'}))

    # 用全局钩子校验两次密码是否一致
    def clean(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if not new_password == confirm_password:
            self.add_error('confirm_password', '两次密码输入不一致')
        return self.cleaned_data
