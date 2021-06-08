
import time

from django import http
from django.shortcuts import render, redirect

# Create your views here.
from dj31.settings import dev

from django.shortcuts import render
# from QQLoginTool.QQtool import oAuthQQ
from django.http import  HttpResponse
from django.views import  View
class QQ_login(View):
    def get(self,request):
        return redirect('https://github.com/')

#IP 多次访问  拒绝  装饰器
def func(fun):
    def fn(request):
        now_time =time.time()
        ip = request.META.get('REMOTE_ADDR')
        if ip not in dev.IP_PULL:
            dev.IP_PULL[ip]=[now_time]
        history=dev.IP_PULL.get(ip)
        while history and now_time-history[-1]>1:
            history.pop()
        if (len(history)) < 3:
            history.insert(0,now_time)
            return fun(request)
        else:
            request.session['black_name']=ip
            request.session.set_expiry(300)
            print('你的短时间访问过多禁止访问')
            return http.HttpResponseForbidden()
    return fn
def blacks(fff):
    def writes(request):
        ip = request.META.get("REMOTE_ADDR")
        black=request.session.get('black_name')
        if ip ==black:
            return http.HttpResponseForbidden('由于你的访问频繁-请于5分钟后登录')
        return fff(request)
    return writes

# 登录装饰器 未登录禁止访问
def login_req(f):
    def func(request):
        if request.user.is_authenticated:
            return f(request)
        else:
            return redirect('/user/login/')

    return func



