import random
import threading
import time

from django.http import JsonResponse

from course.models import Video, Category, Advertisement
# Create your views here.
from course.serializers import CategorySerializer, \
    AdvertisementSerializer, VideoBasicSerializer, VideoSerializer
from panda import cache
from panda.result import Result


def learn(request):
    if request.method == 'GET':
        category_set = Category.objects.all()
        serializer = CategorySerializer(category_set, many=True)
        category_list = serializer.data

        advertisement_set = Advertisement.objects.all()
        serializer = AdvertisementSerializer(advertisement_set, many=True)
        advertisement_list = serializer.data

        learn_model = {
            "category_list": category_list,
            "ad_info": advertisement_list[0]
        }

        return JsonResponse(data=Result(learn_model).to_dict())


def discover(request):
    if request.method == 'GET':
        # viewpager info是首页滚动条，此时用随机数随机查询2个视频。
        last = Video.objects.count() - 1
        index1 = random.randint(0, last)
        index2 = random.randint(0, last - 1)
        if index2 == index1:
            index2 = last
        viewpager1 = VideoBasicSerializer(Video.objects.all()[index1])
        viewpager2 = VideoBasicSerializer(Video.objects.all()[index2])
        viewpager_info = [viewpager1.data, viewpager2.data]
        # new_videos_info返回最新十条的视频
        new_videos = Video.objects.order_by("submission_date")[:10]
        new_videos_info = VideoBasicSerializer(new_videos, many=True).data
        # popular_videos_info返回最火热的十条视频
        popular_videos_info = VideoBasicSerializer(Video.objects.order_by("video_heat")[:10], many=True).data
        discover_model = {
            "viewpager_info": viewpager_info,
            "new_videos_info": new_videos_info,
            "popular_videos_info": popular_videos_info,
        }
        return JsonResponse(data=Result(discover_model).to_dict())


def start_page(request):
    if request.method == 'GET':
        # 启动页图片使用数据库中第一条广告。
        # image_url = Advertisement.objects.first().ad_cover
        image_url = "https://images-public-1306415420.cos.ap-shanghai.myqcloud.com/start_page_image_01.png"
        start_page_model = {
            "image_url": image_url
        }
        return JsonResponse(data=Result(start_page_model).to_dict())


lock = threading.Lock()


def video_player(request):
    if request.method == 'GET':
        video_id = request.GET.get('video_id', default='1')
        with lock:
            while cache.setnx('mysql', '') is not True:
                time.sleep(random.randint(5, 20) * 0.1)
            cache.expire('mysql', 30)
            try:
                video = Video.objects.get(id=video_id)
            except Video.DoesNotExist:
                return JsonResponse(data=Result(message="视频不存在", status=False, code=105).to_dict())
            video.video_heat = video.video_heat + 1
            video.save()
            cache.delete('mysql')

        video_info = VideoSerializer(video).data

        # 视频下方推荐相关视频 目前是返回所有视频中的前10个
        video_suggestions = Video.objects.all()[:10]
        video_suggestion_info = VideoBasicSerializer(video_suggestions, many=True).data
        video_player_model = {
            "video_suggestion_info": video_suggestion_info,
            "video_info": video_info
        }
        return JsonResponse(data=Result(video_player_model).to_dict())


def digg(request):
    play_count = cache.hincrby('video_id1', 'play_count', 1)
    return JsonResponse(Result(data=play_count).to_dict())
