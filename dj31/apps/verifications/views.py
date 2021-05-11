from django.shortcuts import render

# Create your views here.
from django.http import  HttpResponse,JsonResponse
from dj31.utils.captcha.captcha import captcha
from django_redis import  get_redis_connection
import  logging
logger = logging.getLogger('django')
from django.views import View
# from users.models import Users
from  users.models import Users



#图像验证
def Image_code(request,img_id):
    text,image = captcha.generate_captcha()
    #连接数据库
    redis_conn = get_redis_connection('verify')
    #保存 键  过期时间   值
    redis_conn.setex('img_{}'.format(img_id).encode('utf-8'),60,text)
    # 将图片验证码的key和验证码文本保存到redis中，并设置过期时间

    logger.info('图形验证码是_{}.format(text)')

    return HttpResponse(content=image, content_type='image/jpg' )

#用户名
class CheckUsernameView(View):
    """
    Check whether the user exists
    GET username/(?P<username>\w{5,20})/
    """
    def get(self, request, username):

        # count = User.objects.get(username=username).count
        data = {
            'username': username,
            'count': Users.objects.filter(username=username).count()
        }
        return JsonResponse(data=data)
#手机号验证
class CheckMobileView(View):
    """
    检查电话号码是否存在
    """
    def get(self,request,mobile):
        data = {
            'mobile': mobile,
            'count': Users.objects.filter(mobile=mobile).count()
        }
        return  JsonResponse(data=data)