from rest_framework import serializers

from course.models import VideoModel


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoModel
        exclude = ["id"]