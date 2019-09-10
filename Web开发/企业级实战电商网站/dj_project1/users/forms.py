from django import forms
from django.forms import widgets
from users.models import *
from django.forms import fields
from django.core.exceptions import ValidationError


class UserData(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'id':'user_name'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'id':'pwd'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'id':'cpwd'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'id':'email'}))

    # def clean(self):
    #
    #     # 验证邮箱
    #     try:
    #         email = self.cleaned_data['email']
    #     except Exception as e:
    #         raise forms.ValidationError(u"注册账号需为邮箱格式")
    #
    #     # 密码
    #     try:
    #         password1 = self.cleaned_data['password1']
    #     except Exception as e:
    #         print('except: ' + str(e))
    #         raise forms.ValidationError(u"请输入至少6位密码")
    #
    #     if self.cleaned_data['password1'] != self.cleaned_data['password2']:
    #         raise forms.ValidationError(u'确认输入密码不匹配')
        # return self.cleaned_data