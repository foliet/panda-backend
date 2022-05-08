from django.urls import path

from . import views

urlpatterns = [
    path('learn', views.learn),
    path('discover', views.discover),
    path('start_page', views.start_page),
    path('video_player', views.video_player),
    path('digg', views.digg)
]
