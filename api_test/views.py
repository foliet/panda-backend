from django.http import JsonResponse
from django.views import View
# import model
from api_test import models

# Create your views here.


class Hello(View):

    def get(self, request):
        hey= models.HelloModel(str="hello world")
        return JsonResponse({"str":hey.str,"id":hey.id},safe=True)




