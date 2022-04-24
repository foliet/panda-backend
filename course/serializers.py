from rest_framework import serializers

from account_management.models import User
from course.models import Grammar
from course.models import Sentence
from course.models import VideoModel, Category, Advertisement
from course.models import Word


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoModel
        exclude = ["user", "video_heat"]


class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        exclude = ["user"]


class GrammarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grammar
        exclude = ["id"]


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        exclude = ["id"]


class StarSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoModel
        exclude = ["id"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["id"]


class CategorySerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source='id')

    class Meta:
        model = Category
        exclude = ["category_total", "id"]


class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        exclude = ["id"]


class VideoBasicSerializer(serializers.ModelSerializer):
    video_id = serializers.IntegerField(source='id')

    class Meta:
        model = VideoModel
        fields = ["video_cover", "video_title", "video_id"]
