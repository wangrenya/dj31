import logging

from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import render
from django.test import tag
from django.views import View

from dj31.utils.response_code import res_json
from .models import News

logger = logging.getLogger('django')

from . import models
# Create your views here.
def index(request):


    tag =models.Tag.objects.filter(is_delete=False).only('name')
    return render(request,'news/index.html',context={'tags':tag})

class NewsListView(View):
    def get(self,request):
        try:
            tag_id = int(request.GET.get('tag_id',0))
        except Exception as e:
            logger.error('页面或标签定义错误\n{}'.format(e))
            tag_id = 0
        try:
            page = int(request.GET.get('page', 1))
        except Exception as e:
            logger.error('页面或标签定义错误\n{}'.format(e))
            page = 1
        news_list = News.objects.values('title','digest','image_url','update_time','id').annotate(tag_name=F('tag__name'),author=F('author__username'))
        news = news_list.filter(tag_id=tag,id_delete=False) or news_list.filter(id_delete=False)

        pager = Paginator(news,5)
        try:
            news_info = pager.page(page)  # 拿到当前页返回
        except Exception as e:
            logger.error(e)
            news_info = pager.page(pager.num_pages)
        data = {
            'news': list(news_info),
            'total_pages': pager.num_pages
            }
        # return render(request,'news/index.html',context={'data':data})
        return res_json(data=data)