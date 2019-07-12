import re

from django import forms
from django.core.exceptions import ValidationError

from App.models import DfUser


class UserForm(forms.Form):
    username = forms.CharField(min_length=6,error_messages={
        'required':'必须输入用户名',
        'min_length':'用户名不能少于6位'
    })
    password = forms.CharField(min_length=3,error_messages={
        'required':'必须输入密码',
        'min_length':'密码长度不能小于6位'
    })
    confirm_password = forms.CharField(min_length=3,error_messages={
        'required':'必须输入密码',
        'min_length':'密码长度不能小于6位'
    })
    email = forms.EmailField(required=False,error_messages={
        'invalid': "邮箱格式无效"
    })
    phone = forms.CharField(max_length=12,error_messages={
        'max_length':'电话号码不能大于12位'
    })

    def clean_username(self):
        res = DfUser.objects.filter(username=self.cleaned_data.get('username')).exists()
        if res:
            raise ValidationError("用户名重名")
        return self.cleaned_data.get('username')
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        if re.match(r'\d+$',pwd):
            raise ValidationError("密码不能是纯数字")
        return pwd
    def clean(self):
        pwd1 = self.cleaned_data.get('password')
        pwd2 = self.cleaned_data.get('confirm_password')
        if pwd2 != pwd1:
            raise ValidationError({'confirm_password':"两次密码不一致"})
        return self.cleaned_data
    # def clean_phone(self):
    #     value = self.cleaned_data.get('phone')
    #
    #     if not re.match(r"^1[35678]\d{9}$", value):
    #         raise ValidationError("手机号码不正确,请重新填写")
    #     return value
    def clean_email(self):
        em = self.cleaned_data.get('email')

        if not re.match(r"^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$",em):
            raise ValidationError("邮箱格式不正确,请重新填写")
        return em


