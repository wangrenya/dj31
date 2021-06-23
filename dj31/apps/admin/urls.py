from .import views
from django.urls import path,re_path,include


app_name = 'admin'
urlpatterns = [
  path('tagss/<int:tag_id>/',views.TagMangae.as_view(),name='Tag_put'),
  path('tags/',views.TagMangae.as_view(),name='Tag'),
  path('HotNews/',views.HotManage.as_view(),name='HotManage'),
  path('hotnewss/<int:t_id>/',views.HotManage.as_view(),name='hotsnews_edit'),
  re_path('hotsnew/add/',views.HotAddView.as_view(),name='hotsnews_add'),
  path('tags/<int:t_id>/newss/', views.NewsByTagIdView.as_view(), name='news_by_tagid'),
  path('newsmanage/', views.NewsManage.as_view(), name='news_manage'),
  path('newsmanage/<int:t_id>/', views.NewsManage.as_view(), name='news_d' ),
  path('newsedit/<int:e_id>/', views.NewsEdit.as_view(), name='news_edit'),
  path('newsedit/pub/',views.NewsPub.as_view(),name='news_pub'),
  path('newsedit/images/', views.Up_Image_Server.as_view(), name='news_up'),
  path('markdown/', views.MakeDown.as_view(), name='news_down'),
  path('banners/', views.BannerView.as_view(), name='news_banners'),
  path('banners/add/', views.Banneradd.as_view(), name='news_banners_add'),
  path('banners/<int:b_id>/', views.BannerView.as_view(), name='banner_edit'),
  path('banner/<int:t_id>/', views.Banneradd.as_view(), name='banner_add_d'),
  path('docs/', views.DocsManage.as_view(), name='doc_manage'),
  path('docs/<int:d_id>/', views.DocEditView.as_view(), name='doc_edit'),
  path('docs/pub/', views.DocsPub.as_view(), name='docs_pub'),
  path('courses/', views.Coursemanage.as_view(), name='course_manage'),
  path('courses/pub/', views.CoursePubView.as_view(), name='course_pub'),
  path('courses/<int:c_id>/', views.CoursEdit.as_view(), name='course_edit'),
  path('groups/manage/', views.Group_manage.as_view(), name='groups_manage'),
  path('groups/<int:g_id>/', views.Group_edit.as_view(), name='groups_edit'),
  path('groups/add/', views.Group_add.as_view(), name='g_add'),
  path('',views.admin,name='admin'),


]
