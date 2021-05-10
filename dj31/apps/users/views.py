from django.shortcuts import render

# Create your views here.
from django.http import  HttpResponse

# def demo(request):
#     return HttpResponse('hello world')

def index(request):

    return render(request,'news/index.html')
def register(request):

    return render(request,'users/register.html')



