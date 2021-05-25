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
         hot =models.HotNews.objects.only('news__image_url','news__title','news_id').select_related('news').filter(is_delete=False).order_by('priority')[0:3]
         news_click = News.objects.only('title', 'image_url', 'update_time', 'tag__name','author__username').select_related('tag','author').order_by('-clicks')[0:2]
         return render(request,'news/index.html',context={'tags':tag,'click':news_click,'hots':hot})





