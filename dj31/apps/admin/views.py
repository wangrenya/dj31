import json
import logging
from collections import OrderedDict

logger = logging.getLogger('django')
from django.db.models import Count
from django.shortcuts import render, redirect
from django.views import View
from news  import models
#new view 也是引用 qauth view 里面--装饰器
from news.views import login_req
from dj31.utils.response_code import Code,res_json,error_map
from django.utils.decorators import method_decorator
params_status= res_json(errno=Code.PARAMERR,errmsg=error_map[Code.PARAMERR])

@login_req
def admin(request):
    return render(request,'admin/news/index.html')
#文章管理
@method_decorator(login_req,name='get')
class TagMangae(View):
    def get(self,request):
        tags = models.Tag.objects.values('id','name').annotate(num_news=Count('news')).filter(is_delete=False).order_by('num_news')
        return render(request,'admin/news/tag_manage.html',context={'tags':tags})
    def post(self,request):
        js_str=request.body
        if not js_str:
            return params_status
        tag_name =json.loads(js_str)
        name=tag_name.get('name')
        if name:
            name =name.strip()
            tag=models.Tag.objects.get_or_create(name=name)
            return (res_json(errno=Code.OK) if tag[-1] else res_json(errno=Code.DATAEXIST,errmsg='分类名已存在'))
        else:
            return res_json(errno=Code.NODATA,errmsg=error_map[Code.NODATA])
    def put(self,request,tag_id):
        js_str=request.body
        if not js_str:
            return params_status
        dict_data=json.loads(js_str)
        name=dict_data.get('name')
        tag =models.Tag.objects.only('id').filter(is_delete=False,id=tag_id).first()
        if tag:
            if name:
                tag_name= name.strip()
                if  not models.Tag.objects.only('id').filter(name=tag_name).exists():
                    tag.name=tag_name
                    tag.save()
                    return res_json(errno=Code.OK)
                else:
                    return res_json(errno=Code.DATAEXIST, errmsg='分类名文章已存在')
            else:
                return res_json(errno=Code.DATAEXIST,errmsg='分类名已存在')
        else:
            return res_json(errno=Code.PARAMERR, errmsg="需要更新的标签不存在")

    def delete(self,request,tag_id):
         tag=models.Tag.objects.only('id').filter(id=tag_id).first()
         if tag:
             tag.delete()
             return res_json(errmsg="标签更新成功")
         else:
             return res_json(errno=Code.PARAMERR, errmsg="需要删除的标签不存在")
@method_decorator(login_req,name='get')
class HotManage(View):
    def get(self,request):
        hot_news=models.HotNews.objects.only('id','priority','news__title','news__tag__name').select_related('news').filter(is_delete=False).order_by('priority')
        return render(request,'admin/news/HotMangae.html',context={'hot_news':hot_news})
    def put(self,request,h_id):
        json_data = request.body
        if not json_data:
            return params_status
        # 将json转化为dict
        dict_data = json.loads(json_data.decode('utf8'))

        try:
            priority = int(dict_data.get('priority'))
            priority_list = [i for i, _ in models.HotNews.P_CHOICES]
            if priority not in priority_list:
                return res_json(errno=Code.PARAMERR, errmsg='热门文章的优先级设置错误')
        except Exception as e:
            logger.info('热门文章优先级异常：\n{}'.format(e))
            return res_json(errno=Code.PARAMERR, errmsg='热门文章的优先级设置错误')

        hotnews = models.HotNews.objects.only('id').filter(id=h_id,is_delete=False).first()
        if not hotnews:
            return res_json(errno=Code.PARAMERR, errmsg="需要更新的热门文章不存在")

        if hotnews.priority == priority:
            return res_json(errno=Code.PARAMERR, errmsg="热门文章的优先级未改变")

        hotnews.priority = priority
        hotnews.save(update_fields=['priority'])
        return res_json(errmsg="热门文章更新成功")

    def delete(self, request, h_id):
        hotnews = models.HotNews.objects.only('id').filter(id=h_id).first()
        if hotnews:
            hotnews.is_delete = True
            hotnews.save(update_fields=['is_delete'])
            return res_json(errmsg="热门文章删除成功")
        else:
            return res_json(errno=Code.PARAMERR, errmsg="需要删除的热门文章不存在")
@method_decorator(login_req,name='get')
class HotAddView(View):
    def get(self,request):

        tags = models.Tag.objects.values('id', 'name').annotate(num_news=Count('news')). \
        filter(is_delete=False).order_by('-num_news', 'update_time')
        print(tags)
        # 优先级列表
        # priority_list = {K: v for k, v in models.HotNews.PRI_CHOICES}
        priority_dict = OrderedDict(models.HotNews.P_CHOICES)

        return render(request, 'admin/news/hots_newsadd.html', context={'tags':tags,'priority_dict':priority_dict})
    def post(self,request):
        json_data = request.body
        if not json_data:
            return res_json(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
        # 将json转化为dict
        dict_data = json.loads(json_data.decode('utf8'))

        try:
            news_id = int(dict_data.get('news_id'))
        except Exception as e:
            logger.info('前端传过来的文章id参数异常：\n{}'.format(e))
            return res_json(errno=Code.PARAMERR, errmsg='参数错误')

        if not models.News.objects.filter(id=news_id).exists():
            return res_json(errno=Code.PARAMERR, errmsg='文章不存在')

        try:
            priority = int(dict_data.get('priority'))
            priority_list = [i for i, _ in models.HotNews.P_CHOICES]
            if priority not in priority_list:
                return res_json(errno=Code.PARAMERR, errmsg='热门文章的优先级设置错误')
        except Exception as e:
            logger.info('热门文章优先级异常：\n{}'.format(e))
            return res_json(errno=Code.PARAMERR, errmsg='热门文章的优先级设置错误')

        # 创建热门新闻
        hotnews_tuple = models.HotNews.objects.get_or_create(news_id=news_id, priority=priority)
        hotnews, is_created = hotnews_tuple
        hotnews.priority = priority  # 修改优先级
        hotnews.save(update_fields=['priority'])
        return res_json(errmsg="热门文章创建成功")
class NewsByTagIdView(View):
    """
    route: /admin/tags/<int:tag_id>/news/
    """
    def get(self, request, t_id):
        newses = models.News.objects.values('id', 'title').filter(is_delete=False, tag_id=t_id)
        news_list = [i for i in newses]
        print(news_list)
        return res_json(data={
            'news': news_list
        })