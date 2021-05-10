from django.shortcuts import render
from dj31.utils.captcha.captcha import captcha
# Create your views here.
from django.http import  HttpResponse
from django_redis import  get_redis_connection
import  logging
logger = logging.getLogger('django')

# def demo(request):
#     return HttpResponse('hello world')

def index(request):

    return render(request,'news/index.html')
def register(request):

    return render(request,'users/register.html')


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