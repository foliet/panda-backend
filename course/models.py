from django.db import models


# Create your models here.


class Video(models.Model):
    video_title = models.CharField(max_length=100)
    video_level = models.CharField(max_length=20, default='')
    video_cover = models.CharField(max_length=200)
    video_url = models.CharField(max_length=200)
    video_author = models.CharField(max_length=40)
    video_reference = models.CharField(max_length=40, default='')
    submission_date = models.DateTimeField(auto_now_add=True)
    video_description = models.CharField(max_length=200, default='')
    video_heat = models.IntegerField(default=0)


class Sentence(models.Model):
    video = models.ForeignKey('Video', default=None, on_delete=models.CASCADE)
    sentence_content = models.CharField(max_length=100)
    sentence_English = models.CharField(max_length=100)
    sentence_pronunciation = models.CharField(max_length=400)
    sentence_pinyin = models.CharField(max_length=300)
    word = models.ManyToManyField('Word')


class Grammar(models.Model):
    grammar_content = models.CharField(max_length=100)
    grammar_example1 = models.CharField(max_length=100, default='')
    grammar_example2 = models.CharField(max_length=100, default='')
    sentence = models.ForeignKey('Sentence', default=None, on_delete=models.CASCADE)


class Word(models.Model):
    word_content = models.CharField(max_length=10)
    word_spelling = models.CharField(max_length=30)
    word_meaning = models.CharField(max_length=200)
    word_spell_url = models.CharField(max_length=300)


class Category(models.Model):
    category_cover = models.CharField(max_length=200)
    category_title = models.CharField(max_length=15)
    category_description = models.CharField(max_length=200)
    category_author = models.CharField(max_length=15)
    category_total = models.IntegerField()


class Advertisement(models.Model):
    ad_cover = models.CharField(max_length=200, default='')
    ad_url = models.CharField(max_length=200, default='')

