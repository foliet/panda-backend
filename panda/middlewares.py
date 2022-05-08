import traceback

from django.http.response import JsonResponse
from django.middleware.common import MiddlewareMixin

from .result import Result


class ExceptionMiddleware(MiddlewareMixin):
    """统一异常处理中间件"""

    def process_exception(self, request, exception):
        """
        统一异常处理
        :param request: 请求对象
        :param exception: 异常对象
        :return:
        """
        if isinstance(exception, Exception):
            # 服务器异常处理
            print(exception)
            traceback.format_exc()
            return JsonResponse(Result(status=False).to_dict())

        return None
