import re
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from pandaBackend.Result import Result


class LoginCheckMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # | 分隔要匹配的多个url，从左到右匹配，有匹配就返回匹配值，否则返回None。
        pattern = r'/index|/login|/register|/start_page'

        match = re.search(pattern, request.path)
        # 需要拦截的url
        if match or request.session.get('is_login', False):
            pass
        else:
            print('用户未登录URL拦截 >>: ', request.path)
            return JsonResponse(data=Result(message="登录状态有误，请重新登录", status=False, code=104).toDict())
