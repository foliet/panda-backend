from datetime import datetime

from django.db import models
from django.contrib.auth.models import User as User1


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    learner_level = models.CharField(max_length=10)
    points = models.IntegerField()
    country = models.CharField(max_length=30)
    age = models.IntegerField()
    portrait_url = models.CharField(max_length=200)


# 邮箱验证
class EmailVerifyRecord(models.Model):
    # 验证码
    code = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    # 包含注册验证和找回验证
    send_type = models.CharField(max_length=10, choices=(("register", "注册"), ("forget", "找回密码")))
    send_time = models.DateTimeField(default=datetime.now())

    #class Meta:
    #    verbose_name = u"2. 邮箱验证码"
    #    verbose_name_plural = verbose_name

    #def __unicode__(self):
        #return '{0}({1})'.format(self.code, self.email)

