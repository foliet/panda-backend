# Register your models here.
from django.contrib import admin

from .models import VideoModel, Grammar, Category, Sentence, Word, Advertisement

admin.site.register(VideoModel)
admin.site.register(Grammar)
admin.site.register(Category)
admin.site.register(Sentence)
admin.site.register(Word)
admin.site.register(Advertisement)
