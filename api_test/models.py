from django.db import models

# Create your models here.
class HelloModel():
    def __init__(self, str="", id=0):
        self.str=str
        self.id=id

    def __repr__(self):
        return{
            "str":self.str,
            "id":self.id
        }.__str__()



