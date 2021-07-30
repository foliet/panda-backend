import json

from django.http import JsonResponse
from django.views import View
# import model
from api_test import models
from api_test.models import VideoModel


# Create your views here.


class Hello(View):

    def get(self, request):
        hey = models.HelloModel(str="hello world")
        return JsonResponse({"str": hey.str, "id": hey.id}, safe=True)


class Video(View):

    def get(self, request):
        queryset = VideoModel.objects.all()
        video_list = []
        # 序列化
        for video in queryset:
            video_list.append({
                'video_id': video.id,
                'video_title': video.video_title,
                'video_cover': str(video.video_cover),
                'video_url': video.video_url,
                'video_author': video.video_author,
                'video_description': video.video_description,
                'submission_date': video.submission_date
            })

        return JsonResponse(data=video_list, json_dumps_params={'ensure_ascii': False}, safe=False)
