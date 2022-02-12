import json

from django.http import JsonResponse, HttpResponse
from django.views import View
# import model
from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from course import models
from course.models import VideoModel, Sentence, Grammar, Word, Category, Advertisement

# Create your views here.
from course.serializers import VideoSerializer, GrammarSerializer, WordSerializer, CategorySerializer, \
    AdvertisementSerializer
from course.serializers import SentenceSerializer, StarSerializer
from account_management.models import User


class Hello(View):

    def get(self, request):
        hey = models.HelloModel(str="hello world")
        return JsonResponse({"str": hey.str, "id": hey.id}, safe=True)


class VideoLevelList(generics.ListAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            queryset = VideoModel.objects.all()
            level_name = self.request.GET.get('level', None)
            print(level_name)
            if level_name is not None:
                queryset = queryset.filter(video_level=level_name)
                return queryset
            else:
                return JsonResponse('级别为空', safe=False)


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
                'video_level': video.video_level,
                'video_cover': str(video.video_cover),
                'video_url': video.video_url,
                'video_author': video.video_author,
                'video_reference': video.video_reference,
                'video_description': video.video_description,
                'video_heat': video.video_heat,
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
            print(state_name)
            if state_name is not None:
                queryset = queryset.filter(video_title=state_name)
                return queryset
            else:
                return JsonResponse('视频名称为空', safe=False)


class VideoDetail2(generics.ListAPIView):
    serializer_class = VideoSerializer
    queryset = VideoModel.objects.all()
    lookup_field = 'name'

    # 得到一个数据集

    # 得到一个数据集
    def get_queryset(self):
        print(self.kwargs['name'])
        return VideoModel.objects.filter(video_title=self.kwargs['name'])

    # get方法返回一个student
    # def get(self, request, *args, **kwargs):
    #     # 获取url中的参数
    #     # http://127.0.0.1:8000/api/students/aaa/?test=123
    #     # 取test的值
    #     print(self.request.GET.get('test', None))
    #
    #     queryset = self.get_queryset()
    #     serializer = VideoSerializer(queryset, many=True)
    #     return Response({
    #         'data': serializer.data,
    #     })


class SentenceList(generics.ListAPIView):
    queryset = Sentence.objects.all()
    serializer_class = SentenceSerializer

    def get_queryset(self):
        print('printprint')
        if self.request.method == 'GET':
            video_title = self.request.GET.get('video_title', None)
            print(video_title)
            q_set = VideoModel.objects.filter(video_title=video_title)
            video_id = q_set[0].id
            print(video_id)
            return Sentence.objects.filter(video_id=video_id)


# class GrammarList(generics.ListAPIView):
#     queryset = Grammar.objects.all()
#     serializer_class = GrammarSerializer
#
#     def get_queryset(self):
#         if self.request.method == 'GET':
#             video_title = self.request.GET.get('video_title', None)
#             print(video_title)
#             q_set = VideoModel.objects.filter(video_title=video_title)
#             video_id = q_set[0].id
#             q_set = Sentence.objects.filter(video_id=video_id)
#             grammarlist = []
#             for item in q_set:
#                 temp = Grammar.objects.filter(sentence_id=item.id)
#                 for item1 in temp:
#                     grammarlist.append({
#                         "id": item1.id,
#                         "grammar_content": item1.grammar_content,
#                         "grammar_example1": item1.grammar_example1,
#                         "grammar_example2": item1.grammar_example2,
#                         "sentence": item1.sentence
#                     })
#             print(grammarlist)
#             return grammarlist

class GrammarList(View):
    queryset = Grammar.objects.all()
    serializer_class = GrammarSerializer

    def get(self, request):
        if request.method == 'GET':
            video_title = request.GET.get('video_title', None)
            print(video_title)
            q_set = VideoModel.objects.filter(video_title=video_title)
            video_id = q_set[0].id
            q_set = Sentence.objects.filter(video_id=video_id)
            grammarlist = []
            for item in q_set:
                temp = Grammar.objects.filter(sentence_id=item.id)
                for item1 in temp:
                    grammarlist.append({
                        "id": item1.id,
                        "grammar_content": item1.grammar_content,
                        "grammar_example1": item1.grammar_example1,
                        "grammar_example2": item1.grammar_example2,
                        "sentence": item.sentence_content
                    })
            print(grammarlist)
            return JsonResponse(data=grammarlist, json_dumps_params={'ensure_ascii': False}, safe=False)


class WordList(View):
    queryset = Word.objects.all()

    def get(self, request):
        if request.method == 'GET':
            video_title = request.GET.get('video_title', None)
            print(video_title)
            q_set = VideoModel.objects.filter(video_title=video_title)
            video_id = q_set[0].id
            q_set = Sentence.objects.filter(video_id=video_id)
            wordlist = []
            for item in q_set:
                temp = Word.objects.filter(sentence__id=item.id)
                print(temp)
                for item1 in temp:
                    wordlist.append({
                        "id": item1.id,
                        "word_content": item1.word_content,
                        "word_spelling": item1.word_spelling,
                        "word_meaning": item1.word_meaning,
                        "word_spell_url": item1.word_spell_url,
                        "sentence_id": item.id,
                    })
            print(wordlist)
            return JsonResponse(data=wordlist, json_dumps_params={'ensure_ascii': False}, safe=False)


# def get_user_star(request):
#     if request.method == 'GET':
#         user = request.GET.get('email', None)
#         # video_id = video[0]['id']
#         print(user)
#         return HttpResponse('ok')
#     return HttpResponse('0')

class StarList(View):
    queryset = VideoModel.objects.all()

    def get(self, request):
        if request.method == 'GET':
            u = request.session.get('email', None)
            is_login = request.session.get('is_login', None)
            if is_login:
                q_set = VideoModel.objects.filter(user__email=u)
                starlist = []
                for video in q_set:
                    starlist.append({
                        'video_id': video.id,
                        'video_title': video.video_title,
                        'video_cover': str(video.video_cover),
                        'video_url': video.video_url,
                        'video_author': video.video_author,
                        'video_reference': video.video_reference,
                        'video_heat': video.video_heat,
                        'submission_date': video.submission_date,
                    })
                return JsonResponse(data=starlist, json_dumps_params={'ensure_ascii': False}, safe=False)
            else:
                return JsonResponse('用户未登录', safe=False)

    def post(self, request):
        if request.method == 'POST':
            video_title = request.GET.get('video_title', None)
            u = request.session.get('email', None)
            is_login = request.session.get('is_login', None)
            if is_login:
                user = User.objects.get(email=u)
                q_set = VideoModel.objects.filter(video_title=video_title)
                for item in q_set:
                    item.user.add(user)
                return JsonResponse('收藏成功', safe=False)
            else:
                return JsonResponse('用户未登录', safe=False)


class NoteSentenceList(View):
    def get(self, request):
        if request.method == 'GET':
            u = request.session.get('email', None)
            is_login = request.session.get('is_login', None)
            if is_login:
                q_set = Sentence.objects.filter(user__email=u)
                notelist = []
                for sentence in q_set:
                    notelist.append({
                        'video_id': sentence.video_id,
                        'sentence_id': sentence.id,
                        'sentence_content': sentence.sentence_content,
                        'sentence_English': sentence.sentence_English,
                        'sentence_pronunciation': sentence.sentence_pronunciation,
                        'sentence_pinyin': sentence.sentence_pinyin,

                    })
                return JsonResponse(data=notelist, json_dumps_params={'ensure_ascii': False}, safe=False)
            else:
                return JsonResponse('用户未登录', safe=False)

    def post(self, request):
        if request.method == 'POST':
            sentence_id = request.GET.get('sentence_id', None)
            u = request.session.get('email', None)
            is_login = request.session.get('is_login', None)
            if is_login:
                sentence = Sentence.objects.get(id=sentence_id)
                user = User.objects.get(email=u)
                sentence.user.add(user)
                return JsonResponse('添加note成功', safe=False)
            else:
                return JsonResponse('用户未登录', safe=False)


class NoteWordList(View):
    def get(self, request):
        if request.method == 'GET':
            u = request.session.get('email', None)
            is_login = request.session.get('is_login', None)
            if is_login:
                q_set = Word.objects.filter(user__email=u)
                notelist = []
                for item1 in q_set:
                    notelist.append({
                        "id": item1.id,
                        "word_content": item1.word_content,
                        "word_spelling": item1.word_spelling,
                        "word_meaning": item1.word_meaning,
                        "word_spell_url": item1.word_spell_url
                    })
                return JsonResponse(data=notelist, json_dumps_params={'ensure_ascii': False}, safe=False)
            else:
                return JsonResponse('用户未登录', safe=False)

    def post(self, request):
        if request.method == 'POST':
            word_id = request.GET.get('word_id', None)
            u = request.session.get('email', None)
            is_login = request.session.get('is_login', None)
            if is_login:
                word = Word.objects.get(id=word_id)
                user = User.objects.get(email=u)
                word.user.add(user)
                return JsonResponse('添加note成功', safe=False)
            else:
                return JsonResponse('用户未登录', safe=False)


class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            queryset = Category.objects.all()
            return queryset


class AdvertisementList(generics.ListAPIView):
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            queryset = Advertisement.objects.all()
            return queryset




class GetLearnModel(View):
    def get(self, request):
        if request.method == 'GET':
            category_set = Category.objects.all()
            categorylist = []
            for category in category_set:
                categorylist.append({
                    "category_id": category.id,
                    "category_cover": category.category_cover,
                    "category_title": category.category_title,
                    "category_description": category.category_description,
                    "category_author": category.category_author
                })
            advertisement_set = Advertisement.objects.all()
            advertisementlist = []
            for advertisement in advertisement_set:
                advertisementlist.append({
                    "ad_cover": advertisement.ad_cover,
                    "ad_url": advertisement.ad_url,
                })
            learnModel = {
                "category_list": categorylist,
                "ad_info":advertisementlist[0]
            }

            return JsonResponse(data=learnModel, json_dumps_params={'ensure_ascii': False}, safe=False)
