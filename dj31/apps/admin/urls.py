from .import views
from django.urls import path,re_path,include


app_name = 'admin'
urlpatterns = [
  path('tagss/<int:tag_id>/',views.TagMangae.as_view(),name='Tag_put'),
  path('tags/',views.TagMangae.as_view(),name='Tag'),
  path('HotNews/',views.HotManage.as_view(),name='HotManage'),
  path('hotnewss/<int:h_id>/',views.HotManage.as_view(),name='hotsnews_edit'),
  re_path('hotsnew/add/',views.HotAddView.as_view(),name='hotsnews_add'),
  path('tags/<int:t_id>/newss/', views.NewsByTagIdView.as_view(), name='news_by_tagid'),

  path('',views.admin,name='admin'),


]
