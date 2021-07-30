from rest_framework import serializers

from api_test.models import VideoModel


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoModel
        exclude = ["id"]