from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve

from.import views
from dj31.settings import  dev


app_name = 'news'

urlpatterns = [

    path('',views.index,name='index'),
    re_path('news/', views.NewList.as_view(), name='news_list'),
    path('new/<int:news_id>/', views.NewDetail.as_view(), name='n_detail'),
    re_path('new_banner/banners/', views.BannerView.as_view(), name='banner'),
    path('newss/<int:news_id>/comments/', views.CommentsView.as_view(), name='comments'),
    path('search/', views.Searchs(), name='search'),
<<<<<<< HEAD
=======

>>>>>>> courses
    re_path('media/(?P<path>.*)/', serve, {'document_root': dev.MEDIA_ROOT})







]