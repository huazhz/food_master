from django.shortcuts import render
from front import rs






# Create your views here.

def index(req):
    """ 首页 """

    return render(req,'front/index.html')