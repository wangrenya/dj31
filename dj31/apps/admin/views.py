
import json
import logging
from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode

from users.models import Users
from .Forms import NewsPubForm
from .Forms import DocsPubForm
from .Forms import CoursePubForm
from django import http
from django.contrib.auth.models import Group,Permission

from dj31.settings import dev
from dj31.utils.fastdfs.fdfs import FDFS_Client
from .paginator import get_page_data
from django.core.paginator import Paginator, EmptyPage

logger = logging.getLogger('django')
from django.db.models import Count
from django.shortcuts import render
from django.views import View
from news import models
from docs import models as model
from courses import models as mode
#new view 也是引用 qauth view 里面--装饰器
from news.views import login_req
from dj31.utils.response_code import Code,res_json,error_map
from django.utils.decorators import method_decorator
params_status= res_json(errno=Code.PARAMERR,errmsg=error_map[Code.PARAMERR])
from  django.contrib.auth.mixins import  PermissionDenied ,LoginRequiredMixin
from django.contrib.auth.decorators import login_required

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
             tag.is_delete=True
             tag.save(update_fields=['is_delete'])
             return res_json(errmsg="标签更新成功")
         else:
             return res_json(errno=Code.PARAMERR, errmsg="需要删除的标签不存在")

@method_decorator(login_req,name='get')
class HotManage(View):
    def get(self,request):
        hot_news=models.HotNews.objects.only('id','priority','news__title','news__tag__name').select_related('news').filter(is_delete=False).order_by('priority')
        return render(request,'admin/news/HotMangae.html',context={'hot_news':hot_news})
    def put(self,request,t_id):
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

        hotnews = models.HotNews.objects.only('id').filter(id=t_id,is_delete=False).first()
        if not hotnews:
            return res_json(errno=Code.PARAMERR, errmsg="需要更新的热门文章不存在")

        if hotnews.priority == priority:
            return res_json(errno=Code.PARAMERR, errmsg="热门文章的优先级未改变")

        hotnews.priority = priority
        hotnews.save(update_fields=['priority'])
        return res_json(errmsg="热门文章更新成功")
    def delete(self,request,t_id):
        hotnews = models.HotNews.objects.only('id').filter(id=t_id).first()
        if hotnews:
            hotnews.is_delete = True
            hotnews.save(update_fields=['is_delete'])
            return res_json(errmsg="热门文章删除成功")
        else:
            return res_json(errno=Code.PARAMERR, errmsg="需要删除的热门文章不存在")

#热门新闻添加
@method_decorator(login_req,name='get')
class HotAddView(View):
    def get(self,request):
        tags = models.Tag.objects.values('id', 'name').annotate(num_news=Count('news')). \
        filter(is_delete=False).order_by('-num_news', 'update_time')
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

#文章管理
@method_decorator(login_req,name='get')
class NewsManage(View):
    def get(self,request):
        '''
        时间、标题、分类
        '''
        #时间处理
        start_time=request.GET.get('start_time','')
        start_time=datetime.strptime(start_time,'%Y/%m/%d') if start_time else''
        end_time=request.GET.get('end_time','')
        end_time = datetime.strptime(end_time, '%Y/%m/%d') if end_time else''
        newses =models.News.objects.only('title','author__username','tag__name','update_time').filter(is_delete=False)

        if start_time and not end_time:
            newses=newses.filter(update_time__gte=start_time)
        if end_time and not start_time:
            newses=newses.filter(update_time__lte=end_time)
        if start_time and end_time:
            newses=newses.filter(update_time__range=(start_time,end_time))
         #标题处理
        title =request.GET.get('title')
        if title:
            newses=newses.filter(title__icontains=title)
        #作者处理
        author_name=request.GET.get('author_name')
        if author_name:
            newses=newses.filter(author__username__icontains=author_name)
        #处理分类
        tags=models.Tag.objects.only('name').filter(is_delete=False)
        tag_id=request.GET.get('tag_id',0)
        newses=newses.filter(is_delete=False,tag_id=tag_id)  or newses.filter(is_delete=False)
        #处理分页
        try:
            page = int(request.GET.get('page', 1))
        except Exception as e:
            logger.info('页面错误')
            page = 1

        pt = Paginator(newses, 6)
        try:
            news_info = pt.page(page)
        except EmptyPage:
            logger.info('页码错误')
            news_info = pt.page(pt.num_pages)
        # 自定义分页器
        pages_data = get_page_data(pt, news_info)
        # 把日期格式转 字符串格式
        start_time = start_time.strftime('%Y/%m/%d') if start_time else ''
        end_time = end_time.strftime('%Y/%m/%d') if end_time else ''

        data = {
            'news_info': news_info,
            'tags': tags,
            'paginator': pt,
            'start_time': start_time,
            'end_time': end_time,
            'title': title,
            'author_name': author_name,
            'tag_id': tag_id,
            'other_param': urlencode({
                'start_time': start_time,
                'end_time': end_time,
                'title': title,
                'author_name': author_name,
                'tag_id': tag_id,

            })
        }
        data.update(pages_data)

        return render(request, 'admin/news/news_manage.html', context=data)


    def delete(self, request, t_id):
        news = models.News.objects.only('id').filter(id=t_id).first()
        if news:

            news.is_delete = True
            news.save(update_fields=['is_delete'])
            return res_json(errmsg='文章删除成功')
        else:
         return res_json(errno=Code.DATAEXIST, errmsg='删除文章不存在未知的错误存在')

#文章编辑
class NewsEdit(View):
    def get(self,request,e_id):
        news= models.News.objects.filter(id=e_id,is_delete=False).first()

        if news:
            tags=models.Tag.objects.only('name').filter(is_delete=False)
            data = {
                'news':news,
                'tags':tags
            }
            return render(request,'admin/news/news_edit.html',context=data)
        else:
            return res_json(errno=Code.PARAMERR, errmsg='文章不存在')

    def put(self,request,e_id):
        news = models.News.objects.filter(id=e_id, is_delete=False).first()
        if not news:
            return res_json(errno=Code.PARAMERR, errmsg='参数错误')
        js_str = request.body
        if not js_str:
            return res_json(errno=Code.PARAMERR, errmsg='参数错误')
        dict_data = json.loads(js_str)
        if (news.title==dict_data.get('title')and news.digest==dict_data.get('digest')  and news.image_url==dict_data.get('image_url')  ):
            return res_json(errno=Code.PARAMERR,errmsg='文章未做任何更新修改')
        # 清洗数据
        form = NewsPubForm(data=dict_data)


        if form.is_valid():  # True False
            news.title = form.cleaned_data.get('title')
            news.digest = form.cleaned_data.get('digest')
            news.tag = form.cleaned_data.get('tag')
            news.image_url = form.cleaned_data.get('image_url')
            news.content = form.cleaned_data.get('content')
            news.save()
            return res_json(errmsg='文章更新成功')
        else:
            err_m_l = []
            print(1)
            for i in form.errors.values():
                err_m_l.append(i[0])
            err_msg_str = '/'.join(err_m_l)
            return res_json(errno=Code.PARAMERR, errmsg=err_msg_str)
#文章发布
@method_decorator(login_req,name='get')
class NewsPub(View):
    def get(self,request):

        tags = models.Tag.objects.only('id','name').filter(is_delete=False)
        return render(request,'admin/news/news_edit.html',locals())

    def post(self,request):
        """
        获取表单数据
        数据清洗/判断是否合法
        保存到数据库
        :param request:
        :return:
        """
        json_str= request.body
        if not json_str:
            res_json(errno=Code.PARAMERR,errmsg='参数错误')
        dict_data = json.loads(json_str)

        # 数据清洗
        form = NewsPubForm(data=dict_data)
        if form.is_valid():
            # 对于作者更新对于的新闻， 知道新闻是哪个作者发布的
            # 创建实例  保存到数据库
            newss = form.save(commit=False)
            newss.author_id = request.user.id
            newss.tag_id=dict_data.get('tag')
            newss.image_url=dict_data.get('image_url')
            newss.save()
            return res_json(errmsg='文章发布成功')

        else:
            err_m_l = []
            for i in form.errors.values():
                err_m_l.append(i[0])
            err_msg_str = '/'.join(err_m_l)
            return res_json(errno=Code.PARAMERR, errmsg=err_msg_str)

#上传图片到服务器
class Up_Image_Server(View):
    def post(self,request):
        '''图片是image_files 文档  test_files'''
        name = request.FILES
        image_file = name.get('image_files')  if name.get('image_files')  else name.get('text_files')
        if name.get('image_files'):
            if image_file.content_type not in ('image/jpeg', 'image/png', 'image/gif'):
                return res_json(errno=Code.PARAMERR,errmsg='不能传非图片文件')
        if name.get('text_files'):
            if image_file.content_type not in ('application/zip','application/pdf','text/plain'):
                return  res_json(errno=Code.PARAMERR,errmsg='不能传非文档文件')
        # 上传到dfs  ipg  pdf
        ext_name = image_file.name.split('.')[-1]  # jpg
        try:
            upload_img = FDFS_Client.upload_by_buffer(image_file.read(),file_ext_name=ext_name)
        except Exception as e:
            logger.error('文件上传失败{}'.format(e))
            return res_json(errno=Code.UNKOWNERR,errmsg='文件上传失败')
        # 响应
        else:
            if upload_img.get('Status') != 'Upload successed.':
                return res_json(errno=Code.UNKOWNERR,errmsg='文件上传失败')
            else:
                img_id = upload_img.get('Remote file_id')
                img_url = dev.FDFS_URL + img_id  #  拼接地址
                if name.get('image_files'):
                    return res_json(data={'image_url':img_url},errmsg='图片上传成功')
                else:
                    return  res_json(data={'text_url':img_url},errmsg='文档上传成功')

#富文本上传
class MakeDown(View):
    def post(self, request):
        """
        1, 获取参数
        2，验证类型
        3，判断响应
        4，返回
        :param request:
        :return:
        """
        image_file = request.FILES.get('editormd-image-file')
        if not image_file:
            logger.info('从前端获取图片失败')
            return res_json({'success': 0, 'message': '从前端获取图片失败'})

        if image_file.content_type not in ('image/jpeg', 'image/png', 'image/gif'):
            return http.JsonResponse({'success': 0, 'message': '不能上传非图片文件'})

        try:  # jpg
            image_ext_name = image_file.name.split('.')[-1]  # 切割后返回列表取最后一个元素尾缀
        except Exception as e:
            logger.info('图片拓展名异常：{}'.format(e))
            image_ext_name = 'jpg'
        try:
            upload_res = FDFS_Client.upload_by_buffer(image_file.read(), file_ext_name=image_ext_name)
        except Exception as e:
            logger.error('图片上传出现异常：{}'.format(e))
            return http.JsonResponse({'success': 0, 'message': '图片上传异常'})
        else:
            if upload_res.get('Status') != 'Upload successed.':
                logger.info('图片上传到FastDFS服务器失败')
                return http.JsonResponse({'success': 0, 'message': '图片上传到服务器失败'})
            else:
                image_name = upload_res.get('Remote file_id')
                image_url = dev.FDFS_URL + image_name
                return http.JsonResponse({'success': 1, 'message': '图片上传成功', 'url': image_url})
#后台轮播图

class BannerView(View):
    def get(self, request):
        banners = models.Banner.objects.only('id', 'image_url', 'priority').filter(is_delete=False)
        priority_dict = OrderedDict(models.Banner.B_CHOICES)
        return render(request, 'admin/news/news_banners.html', locals())
    def put(self,request,b_id):
        '''获取参数    image    pri   id   验证优先级  处理图片 判断是否有修改'''
        banners = models.Banner.objects.only('id').filter(is_delete=False, id=b_id).first()
        if not banners:
            return res_json(errno=Code.PARAMERR, errmsg='轮播图不存在')

        json_str = request.body
        if not json_str:
            return res_json(errno=Code.PARAMERR, errmsg='获取参数失败')
        dict_data = json.loads(json_str)

        # 获取参数  优先级
        priority = int(dict_data.get('priority'))  # 整形
        priority_list = [i for i, _ in models.Banner.B_CHOICES]  # 作用域

        if priority not in priority_list:
            return res_json(errno=Code.PARAMERR, errmsg='优先级不存在')

        image_url = dict_data['image_url']
        if not image_url:
            return res_json(errno=Code.PARAMERR, errmsg='图片数据为空')

        # 判断是否已修改

        if banners.priority == priority and banners.image_url == image_url:
            return res_json(errno=Code.PARAMERR, errmsg='数据没有修改')

        # 保存到数据库
        banners.priority = priority  # 1 2 3 4  5 6  看他的值
        banners.image_url = image_url

        banners.save(update_fields=['priority', 'image_url'])
        return res_json(errmsg='轮播图更新成功')

#发布轮播图
class Banneradd(View):
    def get(self,request):
        tags=models.Tag.objects.values('id','name').annotate(num_news=Count('news')).filter(is_delete=False)


        pri = OrderedDict(models.Banner.B_CHOICES)
        return render(request,'admin/news/news_banner_add.html',context={'tags':tags,'priority_dict':pri})

    def post(self, request):

        json_str = request.body  # news_id   priority  image_url
        if not json_str:
            return res_json(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])

        dict_data = json.loads(json_str)

        # 校验参数
        news_id = int(dict_data.get('news_id'))

        if not models.News.objects.filter(id=news_id).exists():
            return res_json(errno=Code.PARAMERR, errmsg='新闻不存在')
        try:
            priority = int(dict_data.get('priority'))

            priority_list = [i for i, _ in models.Banner.B_CHOICES]  # 作用域

            if priority not in priority_list:
                return res_json(errno=Code.PARAMERR, errmsg='轮播图优先级错误')
        except Exception as e:
            logger.info('轮播图优先级异常{}'.format(e))
            return res_json(errno=Code.PARAMERR, errmsg='轮播图优先级错误')

        image_url = dict_data.get('image_url')
        if not image_url:
            return res_json(errno=Code.PARAMERR, errmsg='轮播图优先级为空')

        # 创建轮播图  obj  true
        # 创建实例  保存到数据库
        banner = models.Banner.objects.get_or_create(news_id=news_id, priority=priority)

        banners, is_cre = banner
        banners.priority = priority
        banners.image_url = image_url
        banners.save(update_fields=['priority', 'image_url'])
        return res_json(errmsg='轮播图创建成功')

    def delete(self,request,t_id):
        Banner = models.Banner.objects.only('id').filter(id=t_id).first()
        if Banner:

            Banner.is_delete = True
            Banner.save(update_fields=['is_delete'])
            return res_json(errmsg='轮播图删除成功')
        else:
            return res_json(errno=Code.DATAEXIST, errmsg='删除轮播图不存在未知的错误存在')

#文档管理
class DocsManage(View):
    def get(self,request):
        docs=model.Doc.objects.only('id','title','create_time').filter(is_delete=False)
        return render(request,'admin/docs/docs_manage.html',context={'docs':docs})

#文章编辑
class DocEditView(View):
    def get(self,request,d_id):
        doc = model.Doc.objects.filter(is_delete=False,id=d_id).first()
        if doc:
            return render(request,'admin/docs/docs_pub.html',locals())
        else:
            return http.HttpResponseNotFound('PAGE NOT FOUND')
    def put(self,request,d_id):
        docs = model.Doc.objects.filter(is_delete=False, id=d_id).first()
        if not docs:
            return res_json(errno=Code.PARAMERR,errmsg='参数错误')

        js_str=request.body
        dict_data=json.loads(js_str)
        if (docs.title==dict_data.get('title') and  docs.desc==dict_data.get('desc') and docs.file_url==dict_data.get('file_url')  and docs.image_url==dict_data.get('image_url')):
            return res_json(errno=Code.PARAMERR,errmsg='文档未修改')
        form = DocsPubForm(dict_data)
        if form.is_valid():
            for k,v in form.cleaned_data.items():
                setattr(docs,k,v)
            docs.save()
            return res_json(errmsg='文档更新成功')
        else:
            err_m_l = []
            for i in form.errors.values():
                err_m_l.append(i[0])
            err_msg_str = '/'.join(err_m_l)
            return res_json(errno=Code.PARAMERR, errmsg=err_msg_str)
    def delete(self,request,d_id):
        doc = model.Doc.objects.filter(is_delete=False, id=d_id).first()
        if not doc:
            return res_json(Code.PARAMERR,'参数错误')
        doc.is_delete=True
        doc.save(update_fields=['is_delete'])
        return res_json(errmsg='文档删除成功')

#文档发布
class DocsPub(View):
    def get(self,request):
        return render(request,'admin/docs/docs_pub.html')

    def post(self, request):


        js_str = request.body
        if not  js_str:
            return res_json(errno=Code.PARAMERR,errmsg='参数错误')

        dict_data = json.loads(js_str.decode('utf8'))
        form = DocsPubForm(data=dict_data)
        if form.is_valid():
            docs_instance = form.save(commit=False)
            docs_instance.author_id = request.user.id
            docs_instance.save()
            return res_json(errmsg='文档创建成功')
        else:
            # 定义一个错误信息列表
            err_msg_list = []
            for item in form.errors.get_json_data().values():
                err_msg_list.append(item[0].get('message'))
            err_msg_str = '/'.join(err_msg_list)  # 拼接错误信息为一个字符串
            return res_json(errno=Code.PARAMERR, errmsg=err_msg_str)

#在线课程管理
class Coursemanage(View):
    def get(self,request):
        courses=mode.Course.objects.only('title','category__name','teacher__name').select_related('teacher','category').filter(is_delete=False)
        return render(request,'admin/courses/course_manage.html' ,context={'courses':courses})

#课程编辑
class CoursEdit(View):
    def get(self, request,c_id):
        course=mode.Course.objects.only('title').filter(id=c_id,is_delete=False).first()
        if course:
         teachers=mode.Teacher.objects.only('name').filter(is_delete=False)
         categories=mode.CourseCategory.objects.only('name').filter(is_delete=False)
         return render(request, 'admin/courses/course_edit.html',context={'course':course,'teachers':teachers,'categories':categories})
        else:
            return res_json(errno=Code.PARAMERR,errmsg='参数错误')
    def put(self,request,c_id):
        course =mode.Course.objects.filter(id=c_id,is_delete=False).first()
        c=mode.Course.objects.values('teacher').filter(id=c_id).first()
        if not course:
            return res_json(errno=Code.PARAMERR,errmsg='参数错误')
        js_str=request.body
        if not js_str:
            return res_json(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
        dict_data =json.loads(js_str.decode('utf8'))

        t_id=   dict_data.get('teacher')
        d_id=  dict_data.get('category')
        teacher_data=mode.Teacher.objects.filter(id=t_id,is_delete=False).first()
        course_data =mode.CourseCategory.objects.filter(id=d_id,is_delete=False).first()

        if (course.title==dict_data.get('title')and course.category==course_data  and course.teacher==teacher_data and  course.cover_url==dict_data.get('cover_url') and course.video_url==dict_data.get('video_url')  and course.outline==dict_data.get('outline')and course.profile==dict_data.get('profile')):
            return res_json(errno=Code.PARAMERR,errmsg='课程未修改')
        form =CoursePubForm(dict_data)
        if form.is_valid():
            for k, v in form.cleaned_data.items():
                setattr(course,k,v)
            course.save()
            return res_json(errmsg='课程更新成功')

        else:
            err_m_l = []
            for i in form.errors.values():
                err_m_l.append(i[0])
            err_msg_str = '/'.join(err_m_l)
            return res_json(errno=Code.PARAMERR, errmsg=err_msg_str)

    def delete(self,request,c_id):
        course=mode.Course.objects.filter(id=c_id,is_delete=False).first()
        if not course:
            return res_json(errno=Code.DATAEXIST,errmsg='参数错误')
        course.is_delete=True
        course.save(update_fields=['is_delete'])
        return res_json(errmsg='删除课程成功')

#课程发布
class CoursePubView(View):
    def get(self, request):
        teachers = mode.Teacher.objects.only('name').filter(is_delete=False)
        categories = mode.CourseCategory.objects.only('name').filter(is_delete=False)
        return render(request, 'admin/courses/course_edit.html', locals())
    def post(self,request):
        js_str=request.body
        if  not js_str:
            return res_json(errno=Code.DATAEXIST,errmsg='数据错误')
        dict_data=json.loads(js_str.decode('utf8'))
        form=CoursePubForm(dict_data)
        if form.is_valid():
            course_instance=form.save(commit=False)

            course_instance.title=dict_data.get('title')
            course_instance.profile=dict_data.get('profile')
            course_instance.cover_url=dict_data.get('cover_url')
            course_instance.video_url=dict_data.get('video_url')
            course_instance.outline=dict_data.get('outline')
            course_instance.teacher_id=dict_data.get('teacher')
            course_instance.category_id=dict_data.get('category')

            course_instance.save()
            return res_json(errmsg='课程创建成功')

        else:
            err_m_l = []
            for i in form.errors.values():
                err_m_l.append(i[0])
            err_msg_str = '/'.join(err_m_l)
            return res_json(errno=Code.PARAMERR, errmsg=err_msg_str)

#组管理
class Group_manage(View):
    def get(self, request):
        groups=Group.objects.values('id','name').annotate(num_users=Count('user')).order_by('num_users')
        return render(request, 'admin/groups/groups_manage.html',context={'groups':groups})

#组管理添加
class Group_add(View):
    def get(self,request):
        per =Permission.objects.all()
        return render(request,'admin/groups/groups_edit.html' ,context={'permissions':per})
    def post(self,request):
        json_data = request.body
        if not json_data:
            return res_json(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
        dict_data = json.loads(json_data.decode('utf8'))

        # 取出组名，进行判断
        group_name = dict_data.get('name', '').strip()
        if not group_name:
            return res_json(errno=Code.PARAMERR, errmsg='组名为空')

        # 组名存在 false
        one_group, is_created = Group.objects.get_or_create(name=group_name)
        if not is_created:
            return res_json(errno=Code.DATAEXIST, errmsg='组名已存在')

        # 取出权限
        group_permissions = dict_data.get('group_permission')
        if not group_permissions:
            return res_json(errno=Code.PARAMERR, errmsg='权限参数为空')

        try:
            permissions_set = set(int(i) for i in group_permissions)
        except Exception as e:
            logger.info('传的权限参数异常：\n{}'.format(e))
            return res_json(errno=Code.PARAMERR, errmsg='权限参数异常')

        all_permissions_set = set(i.id for i in Permission.objects.only('id'))
        if not permissions_set.issubset(all_permissions_set):
            return res_json(errno=Code.PARAMERR, errmsg='有不存在的权限参数')

        # 设置权限
        for perm_id in permissions_set:
            p = Permission.objects.get(id=perm_id)
            one_group.permissions.add(p)

        one_group.save()
        return res_json(errmsg='组创建成功！')
#组编辑
class Group_edit(View):
    def get(self,request,g_id):
        group = Group.objects.filter(id=g_id).first()
        if group:
            per = Permission.objects.all()
            return render(request,'admin/groups/groups_edit.html',context={'permissions':per,'group':group})
        else:
            return http.HttpResponseForbidden()

    def put(self, request, g_id):
        """
        1, 获取参数   组名  权限
        2，数据清洗
        3，保存
        4，返回

        :param request:
        :param g_id:
        :return:
        """
        group = Group.objects.filter(id=g_id).first()
        if not group:
            return res_json(errno=Code.PARAMERR, errmsg='参数错误')

        js_str = request.body
        dict_data = json.loads(js_str)
        # 组名
        g_name = dict_data.get('name', '').strip()
        if not g_name:
            return res_json(errno=Code.PARAMERR, errmsg='参数错误')
        if g_name != group.name and Group.objects.filter(name=g_name).exists():
            return res_json(errno=Code.DATAEXIST, errmsg='组名存在')

        # 权限校验
        g_permission = dict_data['group_permission']  # [1,2,3,4,5]
        if not g_permission:
            return res_json(errno=Code.PARAMERR, errmsg='参数错误')
        per_set = set(i for i in g_permission) #
        # print(per_set)
        # 去数据库取数据
        db_per_set = set(i.id for i in group.permissions.all())
        if per_set == db_per_set:
            return res_json(errno=Code.DATAEXIST, errmsg='用户在没有修改')
        group.permissions.clear()

        # 设置权限 保存
        for i in per_set:
            p = Permission.objects.get(id=i)
            group.permissions.add(p)

        group.name = g_name
        group.save()
        return res_json(errmsg='组创建成功')


    def delete(self,request,g_id):
        g = Group.objects.filter(id=g_id).first()
        if g:
            g.permissions.clear()
            g.delete()
            return res_json(errmsg='删除成功')
        else:
            return http.HttpResponseForbidden()

#用户管理
class User_manager(View):
    def get(self,request):
        user=Users.objects.only('username','is_staff','is_superuser').filter(is_active=True)


        return  render(request,'admin/groups/users_manage.html',context={'users':user})

#用户编辑
class User_edit(View):
    def get(self,request,u_id):
        user = Users.objects.filter(id=u_id).first()
        if user:
            Groups=Group.objects.only('name').all()
            return render(request,'admin/groups/users_edit.html' ,context={'user_instance':user,'groups':Groups})
        else:
            return res_json(errno=Code.NODATA, errmsg='参数错误')
    def put(self,request,u_id):
        user_instance = Users.objects.filter(id=u_id,is_active=True).first()
        if not user_instance:
            return res_json(errno=Code.NODATA, errmsg='无数据')

        json_str = request.body
        if not json_str:
            return res_json(errno=Code.PARAMERR, errmsg=error_map[Code.NODATA])

        dict_data = json.loads(json_str)
        try:
            groups = dict_data.get('groups')
            is_superuser = int(dict_data['is_superuser'])  # 0
            is_staff = int(dict_data.get('is_staff'))  # 1
            is_active = int(dict_data['is_active'])  # 1
            params = (is_active, is_staff, is_superuser)
            if not all([q in (0, 1) for q in params]):
                return res_json(errno=Code.PARAMERR, errmsg='参数错误')
        except Exception as e:
            logger.info('从前端获取得用户参数错误{}'.format(e))
            return res_json(errno=Code.PARAMERR, errmsg='参数错误')

        try:
            if groups:
                groups_set = set(int(i) for i in groups)
            else:
                groups_set = set()
        except Exception as e:
            logger.info('用户组参数异常{}'.format(e))
            return res_json(errno=Code.PARAMERR, errmsg='用户组参数异常')

        # 组
        all_groups_set = set(i.id for i in Group.objects.only('id'))
        # 判断前台传得组是否在所有用户组里面
        if not groups_set.issubset(all_groups_set):
            return res_json(errno=Code.PARAMERR, errmsg='有不存在的用户组参数')

        gsa = Group.objects.filter(id__in=groups_set)  # [1,3,4]

        # 保存
        user_instance.groups.clear()
        user_instance.groups.set(gsa)
        user_instance.is_staff = bool(is_staff)
        user_instance.is_superuser = bool(is_superuser)
        user_instance.is_active = bool(is_active)
        user_instance.save()
        return res_json(errmsg='用户组更新成功')

    def delete(self,request,u_id):
        user= Users.objects.filter(id=u_id).first()
        if user:
            user.groups.clear()
            user.user_permissions.clear()
            user.is_active=False
            user.delete()     #删除数据库记录
            # user.save()         #单纯修改数据库还有账号信息is_active=False
            return res_json(errmsg='删除成功')
        else:
            return  res_json(errno=Code.NODATA,errmsg='参数错误')