# coding=utf-8
import re
from django.db import models
from django.http import HttpResponse, JsonResponse
from django import forms
from django.views import View
from rest_framework import generics
from rest_framework.utils import json

from account_management.models import User
from account_management.forms import UserForm

# Create your views here.
from course.serializers import UserSerializer


class LoginForm(forms.Form):
    email = forms.CharField(label='邮箱')
    password = forms.CharField(label='密码', widget=forms.PasswordInput())

    def clean_email(self):
        print('clean')
        value = self.cleaned_data['email']
        try:
            result_email = User.objects.get(email=value)
        except User.DoesNotExist:
            raise forms.ValidationError(u"该邮箱未注册", code='email invalid')
        return value

    def clean_password(self):
        value = self.cleaned_data['password']
        if re.match('^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}$', value):
            return value
        else:
            raise forms.ValidationError(u"密码必须由6-20个字母和数字组成", code='password invalid')


def register(request):
    if request.method == 'POST':

        print(request.POST)
        userform = UserForm(request.POST)
        if userform.is_valid():
            print('print')
            print(userform.cleaned_data)
            print('print')
            username = userform.cleaned_data['username']
            password = userform.cleaned_data['password']
            email = userform.cleaned_data['email']
            repeat_password = userform.cleaned_data['repeat_password']
            user = User.objects.create(username=username, password=password, email=email, learner_level='0', points=0,
                                       country='', age=0, portrait_url='http://1.117.107.95/img/portrait.f98bd381.svg')
            user.save()
            return HttpResponse('register success!!!')
        else:
            return HttpResponse(userform.errors.as_json())


def login(request):
    if request.method == 'POST':
        print(request.POST)
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            email = loginform.cleaned_data['email']
            password = loginform.cleaned_data['password']

            user = User.objects.filter(email=email, password=password)

            if user:
                request.session['email'] = email
                request.session['is_login'] = True
                return HttpResponse('登陆成功')
            else:
                return HttpResponse('用户名或密码错误,请重新登录')
        else:
            return HttpResponse(loginform.errors.as_json())


def index(request):
    if request.method == 'GET':
        # 提取浏览器中的cookie，如果不为空，表示已经登录
        u = request.session.get('email', None)
        is_login = request.session.get('is_login', None)
        return JsonResponse('用户{0}的登录状态是{1}'.format(u, is_login), safe=False)


def logout(request):
    request.session.clear()
    return JsonResponse('登出成功', safe=False)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            # 提取浏览器中的cookie，如果不为空，表示已经登录
            u = self.request.session.get('email', None)
            is_login = self.request.session.get('is_login', None)
            if is_login is not None:
                userlist = User.objects.filter(email=u)
                return userlist
            else:
                return []
