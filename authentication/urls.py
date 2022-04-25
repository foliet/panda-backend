from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('verify', views.verify, name='verify'),
    path('register', views.register, name='register'),
    path('index', views.index, name='index'),
    path('logout', views.logout, name='logout'),
]
