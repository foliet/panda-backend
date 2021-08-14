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
from course import views
from account_management import views as views2

urlpatterns = [
    path('admin/', admin.site.urls),
    # 2021.7.23
    path('test/', views.Hello.as_view()),
    # 2021.7.30
    path('videos/', views.VideoList.as_view()),
    # 2021.7.31
    re_path('video/', views.VideoDetail.as_view()),
    path(r'video1/<name>/', views.VideoDetail2.as_view()),
    path(r'register/', views2.register),

    path('login/', views2.login, name='login'),
    path('index/', views2.index, name='index'),
    path('logout/', views2.logout, name='logout'),
    path('course_sentence/',views.SentenceList.as_view()),
    path('course_grammar/',views.GrammarList.as_view()),
    path('course_word/',views.WordList.as_view()),
    path('user_star/',views.StarList.as_view()),
    path('user_sentence_note/',views.NoteSentenceList.as_view()),
    path('user_word_note/',views.NoteWordList.as_view()),
    #
    # path('test1/', views2.Test.as_view())
]
