# Create your tests here.
from django.core.cache import cache
from django.test import TestCase


class MyTest(TestCase):

    def test(self):
        for video in range(4):
            v = {
                'share_count': 0,
                'digg_count': 0,
                'play_count': 0,
            }
            cache.add('video_id{0}'.format(video), v, None)
        print(cache.get('video_id0'))
