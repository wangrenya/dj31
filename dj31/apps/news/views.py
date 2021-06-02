import json
import logging

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import F
from django.shortcuts import render, redirect
from django.test import tag
from django.views import View
from django import http

# import users
from haystack.views import SearchView

from dj31.utils.response_code import res_json, Code, error_map
from .models import News, Banner, Comments

logger = logging.getLogger('django')

from . import models
from django.contrib.auth.decorators import login_required


# Create your views here.
# 登录装饰器
def login_req(f):
    def func(request):
        if request.user.is_authenticated:
            return f(request)
        else:
            return redirect('/user/login/')

    return func

@login_req
def index(request):
     tag =models.Tag.objects.filter(is_delete=False).only('name')
     hot =models.HotNews.objects.only('news__image_url','news__title','news_id').select_related('news').filter(is_delete=False).order_by('priority')[0:3]
     news_click = News.objects.only('title', 'image_url', 'update_time', 'tag__name','author__username').select_related('tag','author').order_by('-clicks')[0:2]
     return render(request,'news/index.html',context={'tags':tag,'click':news_click,'hots':hot})



#新闻列表
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
#新闻详情
class NewDetail(View):
    def  get(self,request,news_id):
        news =News.objects.select_related('author','tag').only('author__username','tag__name','title','content').filter(is_delete=False,id=news_id).first()
        News.in_clicks(news)
        comm =Comments.objects.only('content','author__username','update_time').select_related('author').filter(is_delete=False,news_id=news_id)
        comm_info =[]
        for i in comm:
            comm_info.append(i.to_dict())
        if news:
            return render(request,'news/news_detail.html',context={'news':news,'comm':comm_info})
        else:

            return http.Http404('PAGE NOT FOUND')

#轮播图
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
#追加评论
class CommentsView(View):
    def post(self,request,news_id):
        """
        3 个参数
        新闻ID  评论内容  父评论ID

        1， 判断用户是否登录
        2，获取参数
        3 ，校验参数
        4， 保存到数据库
        :param request:
        :param news_id:
        :return:
        """
        if not request.user.is_authenticated:
            return res_json(errno=Code.SESSIONERR,errmsg=error_map[Code.SESSIONERR])

        if not News.objects.only('id').filter(is_delete=False,id=news_id).exists():
            return res_json(errno=Code.PARAMERR,errmsg=error_map[Code.PARAMERR])

        # 获取参数
        json_data = request.body
        if not json_data:
            return res_json(errno=Code.PARAMERR,errmsg=error_map[Code.PARAMERR])

        dita_data = json.loads(json_data)

        # 一级评论
        content = dita_data['content']
        if not dita_data.get('content'):
            return res_json(errno=Code.PARAMERR,errmsg='评论内容不能为空')

        # 回复评论
        partent_id = dita_data.get('partent_id')
        if partent_id:
            if not Comments.objects.only('id').filter(is_delete=False,id=partent_id,news_id=news_id).exists():
                return res_json(errno=Code.PARAMERR,errmsg=error_map[Code.PARAMERR])
        # 保存数据库
        news_content = Comments()

        news_content.content = content
        print(content)
        news_content.news_id = news_id
        print(news_content.news_id)
        news_content.author = request.user
        news_content.partent_id = partent_id if partent_id else None
        print(news_content.partent_id)
        news_content.save()
        return res_json(data=news_content.to_dict())
#新闻搜索
class Searchs(SearchView):

    template = 'news/search.html'
    def create_response(self):
        query = self.request.GET.get('q','')
        if not query :
            show = True
            hots_news =models.HotNews.objects.select_related('news').only('news_id','news__title','news__image_url').filter(is_delete=False).order_by('priority')
            paginator = Paginator(hots_news, 5)
            try:
                page = paginator.page(int(self.request.GET.get('page', 1)))
            # 假如传的不是整数
            except PageNotAnInteger:
                # 默认返回第一页
                page = paginator.page(1)

            except EmptyPage:
                page = paginator.page(paginator.num_pages)
            return render(self.request, self.template, locals())
        else:
            show = False
            return super().create_response()

