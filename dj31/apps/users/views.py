import re

from django.contrib.auth import login
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection

from dj31.utils.response_code import res_json,Code,error_map
# Create your views here.
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
import json
from django.http import  HttpResponse

# def demo(request):
#     return HttpResponse('hello world')
from users.models import Users
from .forms import LoginForm


def index(request):

    return render(request,'news/index.html')
class RegisView(View):
    def get(self,request):

        return render(request,'users/register.html')
    def post(self,request):
        '''
        "username": sUsername,
      "password": sPassword,
      "password_repeat": sPasswordRepeat,
      "mobile": sMobile,
      "sms_code": sSmsCode
        :param request:
        :return:
        '''
        js_str = request.body
        if not js_str:
            return res_json(errno=Code.PARAMERR, errmsg='参数错误')
        data_dict = json.loads(js_str,strict=False)

        username = data_dict.get('username')
        password = data_dict.get('password')
        password2 = data_dict.get('password_repeat')
        mobile = data_dict.get('mobile')
        sms_code = data_dict.get('sms_code')

        # 1.非空
        if not all([username, password, password2, mobile, sms_code]):
            return HttpResponseForbidden('填写数据不完整')
        # 2.用户名
        if not re.match('^[\u4e00-\u9fa5\w]{5,20}$', username):
            return HttpResponseForbidden('用户名为5-20个字符')
        if Users.objects.filter(username=username).count() > 0:
            return HttpResponseForbidden('用户名已经存在')
        # 密码
        if not re.match('^[0-9A-Za-z]{6,20}$', password):
            return HttpResponseForbidden('密码为6-20个字符')
        # 确认密码
        if password != password2:
            return HttpResponseForbidden('两个密码不一致')
        # 手机号
        if not re.match('^1[3456789]\d{9}$', mobile):
            return HttpResponseForbidden('手机号错误')
        if Users.objects.filter(mobile=mobile).count() > 0:
            return HttpResponseForbidden('手机号存在')
        # 短信验证码
        # 1.读取redis中的短信验证码
        redis_cli = get_redis_connection('verify')
        sms_code_redis = redis_cli.get('sms_{}'.format(mobile))
        # 2.判断是否过期
        if sms_code_redis is None:
            return HttpResponseForbidden('短信验证码已经过期')
        # 3.删除短信验证码，不可以使用第二次
        redis_cli.delete('sms_' + mobile)
        redis_cli.delete('send_flag_' + mobile)
        # 4.判断是否正确
        if sms_code_redis.decode() != sms_code:
            return HttpResponseForbidden('短信验证码错误')
        # 处理
        # 1.创建用户对象
        user = Users.objects.create_user(
            username=username,
            password=password,
            mobile=mobile
        )
        # 2.状态保持
        login(request, user)

        return res_json(errno=Code.OK,errmsg='恭喜贵宾你注册成功')


class LoginView(View):
    def get(self,request):
        return render(request,'users/login.html')
    def  post(self,request):
        js_str=request.body
        if not js_str:
            return res_json(errno=Code.PARAMERR,errmsg='参数错误')
        dict_data= json.loads(js_str.decode())

        #数据验证
        form = LoginForm(data=dict_data,request=request)
        if form.is_valid():
        # 表单验证成工处理
            return res_json(errno=Code.OK,errmsg='贵宾你登录成功')

        else:
        # 表单验证失败处理
            msg_list = []
            for i in form.errors.get_json_data().values():
                msg_list.append(i[0].get('message'))
                msg_str = '/'.join(msg_list)
                return res_json(errno=Code.PARAMERR, errmsg=msg_str)


s=index

