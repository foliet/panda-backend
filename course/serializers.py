from rest_framework import serializers

from course.models import VideoModel, Category
from course.models import Sentence
from course.models import Grammar
from course.models import Word
from account_management.models import User


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoModel
        exclude = ["user", "heat"]


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
    class Meta:
        model = Category
        exclude = ["total"]