from django.shortcuts import render, redirect

# Create your views here.

from django.shortcuts import render
# from QQLoginTool.QQtool import oAuthQQ
from django.http import  HttpResponse
from django.views import  View
class QQ_login(View):
    def get(self,request):
        return redirect('https://github.com/')