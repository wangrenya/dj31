import json

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
                    return res_json(errno=Code.DATAEXIST, errmsg='分类名文章不存在')
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

class HotManage(View):
    def get(self,request):
        hot_news=models.HotNews.objects.only('id','priority','news__title','news__tag__name').select_related('news').filter(is_delete=False).order_by('priority')
        return render(request,'admin/news/HotMangae.html',context={'hot_news':hot_news})


