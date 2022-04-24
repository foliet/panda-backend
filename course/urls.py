from django.urls import path

from . import views

urlpatterns = [
    path('test', views.Hello.as_view()),
    path('learn', views.GetLearnModel.as_view()),
    path('discover', views.GetDiscoverModel.as_view()),
    path('start_page', views.GetStartPageModel.as_view()),
    path('video_player', views.GetVideoPlayerModel.as_view()),
]
