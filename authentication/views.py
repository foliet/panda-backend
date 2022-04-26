# coding=utf-8
import json
import re

from django import forms
from django.contrib.auth import login as sys_login, logout as sys_logout
from django.core.cache import cache
from django.http import JsonResponse

from authentication.email_send import verify_email
from authentication.forms import UserForm
from authentication.models import User
# Create your views here.
from pandaBackend.Result import Result


class LoginForm(forms.Form):
    email = forms.CharField(label='邮箱')
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


def register(request):
    if request.method == 'POST':
        user_form = UserForm(json.loads(request.body.decode()))
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            email = user_form.cleaned_data['email']
            code = user_form.cleaned_data['code']
            code2 = cache.get(email)
            if code2 is None or code != code2:
                return JsonResponse(data=Result(message="验证码错误", status=False, code=107).toDict())
            user = User.objects.create(username=username, password=password, email=email, learner_level='0', points=0,
                                       country='', age=0, avatar_url='http://1.117.107.95/img/portrait.f98bd381.svg')
            user.save()
            return JsonResponse(data=Result(message="register success!!!").toDict())
        else:
            return JsonResponse(data=Result(message="格式错误,或邮箱已注册", status=False, code=103).toDict())


def verify(request):
    if request.method == 'POST':
        user_form = UserForm(json.loads(request.body.decode()))
        if user_form.is_valid():
            email = user_form.cleaned_data['email']
            res_email = verify_email(email, "register")
            if res_email:
                return JsonResponse(data=Result(message="验证码已经发送").toDict())
            else:
                return JsonResponse(data=Result(data=Result(message="验证码发送失败", status=False, code=106).toDict()))
        else:
            return JsonResponse(data=Result(message="格式错误,或邮箱已注册", status=False, code=103).toDict())


def login(request):
    if request.method == 'POST':
        loginform = LoginForm(json.loads(request.body.decode()))
        if loginform.is_valid():
            email = loginform.cleaned_data['email']
            password = loginform.cleaned_data['password']
            user = User.objects.filter(email=email, password=password)
            if user is not None:
                sys_login(request, user[0])
                return JsonResponse(data=Result(user[0].username, message="登陆成功").toDict())
            else:
                return JsonResponse(data=Result(message="用户名或密码错误,请重新登录", status=False, code=101).toDict())
        else:
            return JsonResponse(data=Result(message="用户名或密码错误,请重新登录", status=False, code=101).toDict())


def index(request):
    if request.method == 'GET':
        # 提取浏览器中的cookie，如果不为空，表示已经登录
        user = request.user
        return JsonResponse(Result('用户{0}的登录状态是{1}'.format(user.username, user.is_authenticated)).toDict())


def logout(request):
    if request.method == 'GET':
        sys_logout(request)
        return JsonResponse(Result('登出成功').toDict())

# class UserList(generics.ListAPIView):
#    serializer_class = UserSerializer
#
#    def get_queryset(self):
#        if self.request.method == 'GET':
#            # 提取浏览器中的cookie，如果不为空，表示已经登录
#            u = self.request.session.get('email', None)
#            is_login = self.request.session.get('is_login', None)
#            if is_login is not None:
#                userlist = User.objects.filter(email=u)
#                return userlist
#            else:
#                return []
#
