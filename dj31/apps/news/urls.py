from django.urls import path,re_path,include
from . import  views

app_name='news'
urlpatterns = [
    re_path('',views.index),
    path('news/', views.NewsListView.as_view(), name='news_list'),

]
