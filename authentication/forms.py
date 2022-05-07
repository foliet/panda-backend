# coding=utf-8
import re

from django import forms

from authentication.models import User


class UserForm(forms.Form):
    # class Meta:
    #     model = User
    #     fields = ['username','email','password','repeat_password']
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=50)
    repeat_password = forms.CharField(max_length=100)
    code = forms.CharField(max_length=20, required=False)

    def clean_email(self):
        value = self.cleaned_data['email']
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            return value
        raise forms.ValidationError(u"该邮箱已注册", code='email invalid')

    def clean_password(self):
        value = self.cleaned_data['password']
        if re.match('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z!@#$%&*_]{6,20}$', value):
            return value
        else:
            raise forms.ValidationError(u"密码必须由6-20个字母和数字或!@#$%&*_组成", code='password invalid')

    def clean_repeat_password(self):
        value = self.cleaned_data['repeat_password']
        password = self.cleaned_data['password']
        if password and value and password != value:
            raise forms.ValidationError(u"两次输入的值不相同", code='repeat_password invalid')
        return value

    def clean_username(self):
        value = self.cleaned_data['username']
        try:
            User.objects.get(username=value)
        except User.DoesNotExist:
            if re.match("^[A-Za-z\u4e00-\u9fa5][a-zA-Z0-9_\u4e00-\u9fa5]*$", value):
                return value
            else:
                raise forms.ValidationError("用户名只能有汉字字母数字下划线组成")
        raise forms.ValidationError('该用户名已注册')


class LoginForm(forms.Form):
    email = forms.EmailField(label='邮箱')
    password = forms.CharField(label='密码', widget=forms.PasswordInput())

    def clean_email(self):
        value = self.cleaned_data['email']
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise forms.ValidationError(u"该邮箱未注册", code='email invalid')
        return value

    def clean_password(self):
        value = self.cleaned_data['password']
        # 这个正则表达式不一定对
        if re.match('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z!@#$%&*_]{6,20}$', value):
            return value
        else:
            raise forms.ValidationError(u"密码必须由6-20个字母和数字或!@#$%&*_组成", code='password invalid')


class EmailForm(forms.Form):
    email = forms.EmailField(label='邮箱')

    def clean_email(self):
        value = self.cleaned_data['email']
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            return value
        raise forms.ValidationError(u"该邮箱已注册", code='email invalid')
