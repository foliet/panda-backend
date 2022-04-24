import random

from django.http import JsonResponse
from django.views import View
from rest_framework import generics

from course.models import VideoModel, Category, Advertisement
# Create your views here.
from course.serializers import VideoSerializer, CategorySerializer, \
    AdvertisementSerializer, VideoBasicSerializer
from pandaBackend.Result import Result


class Hello(View):
    def get(self, request):
        result = Result(data="hello world").toDict()
        return JsonResponse(result, safe=False)


class GetLearnModel(generics.GenericAPIView):
    def get(self, request):
        if request.method == 'GET':
            self.serializer_class = CategorySerializer
            category_set = Category.objects.all()
            serializer = self.get_serializer(category_set, many=True)
            categorylist = serializer.data

            self.serializer_class = AdvertisementSerializer
            advertisement_set = Advertisement.objects.all()
            serializer = self.get_serializer(advertisement_set, many=True)
            advertisementlist = serializer.data

            learnModel = {
                "category_list": categorylist,
                "ad_info": advertisementlist[0]
            }

            return JsonResponse(data=Result(learnModel).toDict())


class GetDiscoverModel(generics.GenericAPIView):
    def get(self, request):
        if request.method == 'GET':
            self.serializer_class = VideoBasicSerializer
            # viewpager info是首页滚动条，此时用随机数随机查询2个视频。
            last = VideoModel.objects.count() - 1
            index1 = random.randint(0, last)
            index2 = random.randint(0, last - 1)
            if index2 == index1:
                index2 = last
            viewpager1 = self.get_serializer(VideoModel.objects.all()[index1])
            viewpager2 = self.get_serializer(VideoModel.objects.all()[index2])
            viewpager_info = [viewpager1.data, viewpager2.data]
            # new_videos_info返回最新十条的视频
            new_videos = VideoModel.objects.order_by("submission_date")[:10]
            new_videos_info = self.get_serializer(new_videos, many=True).data
            # popular_videos_info返回最火热的十条视频
            popular_videos_info = self.get_serializer(VideoModel.objects.order_by("video_heat")[:10], many=True).data
            discoverModel = {
                "viewpager_info": viewpager_info,
                "new_videos_info": new_videos_info,
                "popular_videos_info": popular_videos_info,
            }
            return JsonResponse(data=Result(discoverModel).toDict())


class GetStartPageModel(generics.GenericAPIView):
    def get(self, request):
        if request.method == 'GET':
            # 启动页图片使用数据库中第一条广告。
            # image_url = Advertisement.objects.first().ad_cover
            image_url = "https://images-public-1306415420.cos.ap-shanghai.myqcloud.com/start_page_image_01.png"
            startPageModel = {
                "image_url": image_url
            }
            return JsonResponse(data=Result(startPageModel).toDict())


class GetVideoPlayerModel(generics.GenericAPIView):
    def get(self, request):
        if request.method == 'GET':
            video_id = request.GET.get('video_id', default='-1')
            try:
                video = VideoModel.objects.get(id=video_id)
            except VideoModel.DoesNotExist:
                return JsonResponse(data=Result(message="视频不存在", status=False, code=105).toDict())
            self.serializer_class = VideoSerializer
            video_info = self.get_serializer(video).data

            # 视频下方推荐相关视频 目前是返回所有视频中的前10个
            video_suggestions = VideoModel.objects.all()[:10]
            self.serializer_class = VideoBasicSerializer
            video_suggestion_info = self.get_serializer(video_suggestions, many=True).data
            videoPlayerModel = {
                "video_suggestion_info": video_suggestion_info,
                "video_info": video_info
            }
            return JsonResponse(data=Result(videoPlayerModel).toDict())
