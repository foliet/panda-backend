from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# 注册模块
from django.views import View
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from account_management.serializers import AccountSerializer, AccountFrom
from django.contrib.auth.hashers import make_password, check_password


class AccountDetail(generics.CreateAPIView):
    serializer_class = AccountSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = AccountSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def login(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        print(username)
        password = request.GET.get('password')
        print(password)
        user = User.objects.get(username=username)
        print(user)
        password1 = User.objects.get(username=username).password
        print(password1)
        pwd_bool = check_password(password, password1)
        print(pwd_bool)

        if user:
            if pwd_bool:
                request.session['username'] = username
                request.session['is_login'] = True
                return JsonResponse('登录成功', safe=False)
            else:
                return JsonResponse('密码错误', safe=False)
        else:
            return JsonResponse('用户名不存在', safe=False)


# 通过cookie判断用户是否已登录
def index(request):
    if request.method == 'GET':
        # 提取浏览器中的cookie，如果不为空，表示已经登录
        u = request.session.get('username', None)
        is_login = request.session.get('is_login', None)
        return JsonResponse('用户{0}的登录状态是{1}'.format(u, is_login), safe=False)


def logout(request):
    request.session.clear()
    return JsonResponse('登出成功', safe=False)


class Test(View):
    def post(self, request):
        uu = self.request.POST.get('username')
        print(uu)
        return HttpResponse(uu, status=400)
