import logging

from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import render
from django.test import tag
from django.views import View
from django import http

from dj31.utils.response_code import res_json
from .models import News, Banner

logger = logging.getLogger('django')

from . import models
# Create your views here.
class IndexView(View):
    def get(self,request):
        tag =models.Tag.objects.filter(is_delete=False).only('name')
<<<<<<< HEAD
        return render(request,'news/index.html',context={'tags':tag})

# class NewList(View):
#     def get(self,request):
#         '''
#         router:/news/
#         :param request:
#         :return:
#         '''
#         try:
#             tag= int(request.GET.get('tag_id', 0))
#         except Exception as e:
#             logger.error('页面或标签定义错误\n{}'.format(e))
#             tag= 0
#         try:
#             page =int(request.GET.get('page',1))
#         except Exception as e:
#             logger.error('页码错误{}'.format(e))
#             page = 1
#         news_list = News.objects.values('title','digest','image_url','update_time','id').annotate(tag_name=F('tag__name'),author=F('author__username'))
#         news = news_list.filter(tag_id=tag,is_delete=False) or news_list.filter(is_delete=False)
#         #分页
#
#         pages =Paginator(news,5)
#         try:
#             news =pages.page(page)
#         except Exception as  e:
#             logger.error(e)
#             news = pages.page(pages.num_pages)
#         data={
#             'news':list(news),
#             'total_pages':pages.num_pages
#         }
#         return res_json(data=data)


# class BannerView(View):
#     def get(self,request):
#         banner = models.Banner.objects.only('image_url','news__title').select_related('news').filter(id_delete=False).order_by('priority')  # 从1到6
#         banner_info = []
#         for i in banner:
#             banner_info.append({
#                 'image_url': i.image_url,
#                 'news_title': i.news.title,
#                 'news_id': i.news.id
#             })
#         data = {
#             'banners': banner_info
#         }
#         return res_json(data=data)
=======
        hot =models.HotNews.objects.only('news__image_url','news__title','news_id').select_related('news').filter(is_delete=False).order_by('priority')[0:3]
        news_click = News.objects.only('title', 'image_url', 'update_time', 'tag__name','author__username').select_related('tag','author').order_by('-clicks')[0:2]
        return render(request,'news/index.html',context={'tags':tag,'click':news_click,'hots':hot})





>>>>>>> news
