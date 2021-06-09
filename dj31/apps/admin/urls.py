from .import views
from django.urls import path,re_path,include




app_name = 'admin'
urlpatterns = [
  path('tagss/<int:tag_id>/',views.TagMangae.as_view(),name='Tag_put'),
  path('tags/',views.TagMangae.as_view(),name='Tag'),
  path('HotNews/',views.HotManage.as_view(),name='HotManage'),
  path('',views.admin,name='admin'),


]
