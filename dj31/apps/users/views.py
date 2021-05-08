from django.shortcuts import render

# Create your views here.
from django.http import  HttpResponse
def demo(request):
    return HttpResponse('hello world')
