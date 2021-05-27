from django.urls import path,re_path
from django.views.static import serve
from dj31.settings import dev
from . import  views


app_name = 'verifications'
urlpatterns = [
    path('image_code/<uuid:img_id>/', views.Image_code, name='image_code'),
    re_path('username/(?P<username>\w{5,20})/', views.CheckUsernameView.as_view(), name='check_username'),
    re_path('mobile/(?P<mobile>1[3-9]\d{9})/', views.CheckMobileView.as_view(), name='check_mobile'),
    re_path('sms_code/', views.SmsCodeView.as_view(), name='sms_code'),
    re_path('news/', views.NewList.as_view(), name='news_list'),
    path('new/<int:news_id>/', views.NewDetail.as_view(), name='n_detail'),
    re_path('new_banner/banners/', views.BannerView.as_view(), name='banner'),
    path('newss/<int:news_id>/comments/', views.CommentsView.as_view(), name='comments'),
    re_path('media/(?P<path>.*)/', serve, {'document_root': dev.MEDIA_ROOT}),





 ]