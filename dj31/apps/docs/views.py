from django.shortcuts import render
from  dj31.settings.dev import FILE_URL
# Create your views here.
from django.views import View
from django import http
from .models import Doc
from django.utils.encoding import escape_uri_path
import requests
def docs(request):
    docs =Doc.objects.only('title','desc','image_url').filter(is_delete=False)
    return render(request,'doc/docDownload.html',context={'docs':docs})
def ds(request,d_id):
    doc_file=Doc.objects.only('file_url').filter(is_delete=False,id=d_id).first()
    if doc_file:
        doc_url=doc_file.file_url
        doc_url =FILE_URL + doc_url
        res =http.FileResponse(requests.get(doc_url,stream=True))
        ex_name =doc_url.split('.')[-1]#pdf
        if not ex_name:
            raise http.Http404('文件名异常')
        else:
            ex_name=ex_name.lower()
        if ex_name =='pdf':
            res['Content-type']='application/pdf'
        elif ex_name =='doc':
            res['Content-type'] = 'application/msowrd'
        else:
            raise http.Http404('文件格式错误')
        doc_filename=escape_uri_path(doc_url.split('/')[-1])
        res["Content-Disposition"] = "attachment; filename*=UTF-8''{}".format(doc_filename)

        return res
    else:
        raise http.Http404('文档不存在')

load = ds




