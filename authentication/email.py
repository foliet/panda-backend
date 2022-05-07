from random import Random  # 用于生成随机码

from django.conf import settings  # setting.py添加的的配置信息
from django.core.cache import cache
from django.core.mail import send_mail  # 发送邮件模块


# 生成随机字符串
def random_str(random_length=8):
    """
    随机字符串
    :param random_length: 字符串长度
    :return: String 类型字符串
    """
    _str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        _str += chars[random.randint(0, length)]
    return _str


# 发送电子邮件
def verify_email(email, send_type="register"):
    """
    发送电子邮件
    :param email: 要发送的邮箱
    :param send_type: 邮箱类型
    :return: True/False
    """
    # 将给用户发的信息保存在数据库中
    code = random_str(5)
    cache.set(email, code, 300)
    # 如果为注册类型
    if send_type == "register":
        email_title = "注册激活"
        # email_body = "请点击下面的链接激活你的账号:http://127.0.0.1:8000/active/{0}".format(code)
        email_body = "您的邮箱注册验证码为：{0}, 该验证码有效时间为5分钟，请及时进行验证。".format(code)
        # 发送邮件
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if not send_status:
            return False
    if send_type == "retrieve":
        email_title = "找回密码"
        email_body = "您的邮箱召回验证码为：{0}, 该验证码有效时间为5分钟，请及时进行验证。".format(code)
        # 发送邮件
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if not send_status:
            return False
    return True
