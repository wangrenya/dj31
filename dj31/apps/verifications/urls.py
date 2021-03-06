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
    re_path('media/(?P<path>.*)/', serve, {'document_root': dev.MEDIA_ROOT}),





 ]