import json

import django
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.http import JsonResponse

from authentication.email import verify_email
from authentication.forms import UserForm, LoginForm, EmailForm
from authentication.models import User
from panda.result import Result


def register(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            user_form = UserForm(json.loads(request.body.decode()))
        else:
            user_form = UserForm(request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            email = user_form.cleaned_data['email']
            code = user_form.cleaned_data['code']
            code2 = cache.get(email)
            if code2 is None or code != code2:
                return JsonResponse(data=Result(message="验证码错误", status=False, code=107).to_dict())
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return JsonResponse(data=Result(message="register success!!!").to_dict())
        else:
            return JsonResponse(data=Result(message="格式错误,或邮箱已注册", status=False, code=103).to_dict())


def verify(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            email_form = EmailForm(json.loads(request.body.decode()))
        else:
            email_form = EmailForm(request.POST)
        if email_form.is_valid():
            email = email_form.cleaned_data['email']
            res_email = verify_email(email, "register")
            if res_email:
                return JsonResponse(data=Result(message="验证码已经发送").to_dict())
            else:
                return JsonResponse(data=Result(data=Result(message="验证码发送失败", status=False, code=106).to_dict()))
        else:
            return JsonResponse(data=Result(message="格式错误,或邮箱已注册", status=False, code=103).to_dict())


def login(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            login_form = LoginForm(json.loads(request.body.decode()))
        else:
            login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                django.contrib.auth.login(request, user)
                return JsonResponse(data=Result(user.username, message="登陆成功").to_dict())
            else:
                return JsonResponse(data=Result(message="用户名或密码错误,请重新登录", status=False, code=101).to_dict())
        else:
            return JsonResponse(data=Result(message="用户名或密码错误,请重新登录", status=False, code=101).to_dict())
    if request.method == 'GET':
        return JsonResponse(
            data=Result({"signup_url": "http://101.43.15.9/signup", "retrieve_password_url": "456"}).to_dict())


def index(request):
    if request.method == 'GET':
        # 提取浏览器中的cookie，如果不为空，表示已经登录
        user = request.user
        return JsonResponse(Result('用户{0}的登录状态是{1}'.format(user.username, user.is_authenticated)).to_dict())


def logout(request):
    if request.method == 'GET':
        django.contrib.auth.logout(request)
        return JsonResponse(Result('登出成功').to_dict())

# class UserList(generics.ListAPIView):
#    serializer_class = UserSerializer
#
#    def get_queryset(self):
#        if self.request.method == 'GET':
#            # 提取浏览器中的cookie，如果不为空，表示已经登录
#            u = self.request.session.get('email', None)
#            is_login = self.request.session.get('is_login', None)
#            if is_login is not None:
#                user_list = User.objects.filter(email=u)
#                return user_list
#            else:
#                return []
#
