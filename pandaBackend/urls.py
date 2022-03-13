"""pandaBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
# 2021.7.23
from course import views as course_views
from account_management import views as account_management_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', course_views.Hello.as_view()),
    path('login/', account_management_views.login, name='login'),
    path('index/', account_management_views.index, name='index'),
    path('logout/', account_management_views.logout, name='logout'),
    path('learn/', course_views.GetLearnModel.as_view()),
    path('discover/', course_views.GetDiscoverModel.as_view())
    #
    # path('test1/', views2.Test.as_view())
]
