import http

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.views import View

from .models import Course

def video(request):
    return render(request,'course/video_test.html')

def videos(request):
    courses = Course.objects.only('title','id','cover_url','teacher__name').select_related('teacher').filter(is_delete=False)
    return render(request,'course/course.html',context={'courses':courses})
class Course_detail(View):
    def get(self,request,c_id):
        course =Course.objects.only('title','cover_url','video_url','profile','teacher__profile','outline','teacher__name','teacher__avatar_url','teacher__pos_title','teacher__profile').select_related('teacher').filter(is_delete=False,id=c_id).first()
        if course:
            return render(request,'course/course_detail.html',context={'course':course})
        else:
            raise http.Http404('NOT FOUND PAGE')



