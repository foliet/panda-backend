import json

from django.http import JsonResponse, HttpResponse
from django.views import View
# import model
from rest_framework import status, generics
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from api_test import models
from api_test.models import VideoModel

# Create your views here.
from api_test.serializers import VideoSerializer


class Hello(View):

    def get(self, request):
        hey = models.HelloModel(str="hello world")
        return JsonResponse({"str": hey.str, "id": hey.id}, safe=True)


class VideoList(View):
    queryset = VideoModel.objects.all()

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

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        serializer = VideoSerializer(data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, status=201)
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, status=400)


class VideoDetail(generics.ListAPIView):
    serializer_class = VideoSerializer

    # 得到一个数据集

    def get_queryset(self):
        if self.request.method == 'GET':
            queryset = VideoModel.objects.all()
            state_name = self.request.GET.get('q', None)
            if state_name is not None:
                queryset = queryset.filter(video_title=state_name)
                return queryset


class VideoDetail2(generics.ListAPIView):
    serializer_class = VideoSerializer
    queryset = VideoModel.objects.all()
    lookup_field = 'name'
    # 得到一个数据集

    # 得到一个数据集
    def get_queryset(self):
        return VideoModel.objects.filter(video_title=self.kwargs['name'])

    # get方法返回一个student
    def get(self, request, *args, **kwargs):
        # 获取url中的参数
        # http://127.0.0.1:8000/api/students/aaa/?test=123
        # 取test的值
        print(self.request.GET.get('test', None))

        queryset = self.get_queryset()
        serializer = VideoSerializer(queryset, many=True)
        return Response({
            'data': serializer.data,
        })
