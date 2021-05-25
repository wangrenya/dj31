<<<<<<< HEAD
=======
import http

>>>>>>> news
from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import render


# Create your views here.
from django.http import  HttpResponse,JsonResponse
from  celery_tasks.sms.tasks import send_sms_code
from dj31.utils.captcha.captcha import captcha
from django_redis import  get_redis_connection
import json
import  logging
import random

from dj31.utils.response_code import res_json,Code,error_map
from dj31.utils.yuntongxun.sms import CCP
from news.models import News
<<<<<<< HEAD
=======
from news.models import Banner

from . import  models
>>>>>>> news

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
    redis_conn.setex('img_{}'.format(img_id).encode('utf-8'),300,text)
    # 将图片验证码的key和验证码文本保存到redis中，并设置过期时间

    # logger.info('图形验证码是_{}.format(text)')
    logger.info('图形验证码是:{}'.format(text ))

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
        return JsonResponse(data=data)
#短信验证码
class SmsCodeView(View):
    def post(self,request):

        '''手机号   uuid   图形验证码'''

        #接收参数
        json_str =request.body
        if not json_str:
            return res_json(errno=Code.PARAMERR,errmsg='参数错误')

        dict_data = json.loads(json_str,strict=False)
        image_code_client = dict_data.get('text')
        uuid = dict_data.get('image_code_id')
        mobile = dict_data.get('mobile')
        #参数验证
        if not all([image_code_client, uuid, mobile]):
            return res_json(errno=Code.PARAMERR, errmsg='参数错误')

        # 创建连接到redis的对象
        redis_conn = get_redis_connection('verify')
       # 提取数据库的图形验证码
        image_code_server = redis_conn.get('img_{}'.format(uuid))
        if image_code_server is None:
        # 图形验证码过期或者不存在
            return res_json(errno=Code.PARAMERR, errmsg='参数错误')
        # 删除图形验证码，避免恶意测试图形验证码
        try:
         redis_conn.delete('img_{}' .format('uuid'))
        except Exception as e:
         logger.error(e)
        # 对比图形验证码
        image_code_server = image_code_server.decode()  # bytes转字符串
        if image_code_client.lower() != image_code_server.lower():  # 转小写后比较
            return res_json(errno=Code.PARAMERR, errmsg='输入图形验证码有误')

        # 生成短信验证码：生成6位数验证码
        sms_code = '%06d' % random.randint(0, 999999)

        # 限定频繁发送验证码
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return res_json(errno=Code.DATAEXIST, errmsg='发送短信过于频繁')

        redis_conn.setex('sms_%s' % mobile, 300, sms_code)
        # 重新写入send_flag
        redis_conn.setex('send_flag_%s' % mobile, 500, 1)
        # 执行请求
        # 发送短信
        logger.info('短信验证码: {}'.format(sms_code))
        logging.info('发送短信正常[mobile:%s sms_num:%s]' % (mobile, sms_code))

    # 发送短信验证码
    #     ccp = CCP()
    #     ccp.send_template_sms(mobile, [sms_code, 5], 1)
    # 响应结果
        send_sms_code.delay(mobile,sms_code)
        return res_json(errmsg='短信验证码发送成功')

class NewList(View):
    def get(self,request):
        '''
        router:/news/
        :param request:
        :return:
        '''
        try:
            tag= int(request.GET.get('tag_id', 0))
        except Exception as e:
            logger.error('页面或标签定义错误\n{}'.format(e))
            tag= 0
        try:
            page =int(request.GET.get('page',1))
        except Exception as e:
            logger.error('页码错误{}'.format(e))
            page = 1
        news_list = News.objects.values('title','digest','image_url','update_time','id').annotate(tag_name=F('tag__name'),author=F('author__username'))
        news = news_list.filter(tag_id=tag,is_delete=False) or news_list.filter(is_delete=False)
        #分页

<<<<<<< HEAD
=======
# news
class NewList(View):
    def get(self,request):
        '''
        router:/news/
        :param request:
        :return:
        '''
        try:
            tag= int(request.GET.get('tag_id', 0))
        except Exception as e:
            logger.error('页面或标签定义错误\n{}'.format(e))
            tag= 0
        try:
            page =int(request.GET.get('page',1))
        except Exception as e:
            logger.error('页码错误{}'.format(e))
            page = 1
        news_list = News.objects.values('title','digest','image_url','update_time','id').annotate(tag_name=F('tag__name'),author=F('author__username'))
        news = news_list.filter(tag_id=tag,is_delete=False) or news_list.filter(is_delete=False)
        #分页

>>>>>>> news
        pages =Paginator(news,5)
        try:
            news =pages.page(page)
        except Exception as  e:
            logger.error(e)
            news = pages.page(pages.num_pages)
        data={
            'news':list(news),
            'total_pages':pages.num_pages
        }
        return res_json(data=data)
<<<<<<< HEAD
=======

class NewDetail(View):
    def  get(self,request,news_id):
        news =News.objects.select_related('author','tag').only('author__username','tag__name','title','content').filter(is_delete=False,id=news_id).first()
        a=news.clicks
        News.in_clicks(news)
        if news:
            return render(request,'news/news_detail.html',context={'news':news})
        else:

            return http.Http404('PAGE NOT FOUND')
class BannerView(View):
    def get(self,request):
        banner = Banner.objects.select_related('news').only('image_url','news__title').filter(is_delete=False).order_by('priority')
        banner_info = []
        for i in banner:
            banner_info.append({
                'image_url': i.image_url,
                'news_title': i.news.title,
                'news_id': i.news.id
            })
        data = {
            'banners': banner_info
        }
        return res_json(data=data)
>>>>>>> news
