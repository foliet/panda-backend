from django.db import models


# Create your models here.
class HelloModel():
    def __init__(self, str="", id=0):
        self.str = str
        self.id = id

    def __repr__(self):
        return {
            "str": self.str,
            "id": self.id
        }.__str__()


class VideoModel(models.Model):

    video_title = models.CharField(max_length=100)
    video_cover = models.CharField(max_length=200)
    video_url = models.CharField(max_length=200)
    video_author = models.CharField(max_length=40)
    video_description = models.CharField(max_length=400)
    submission_date = models.DateTimeField(auto_now_add=True)
