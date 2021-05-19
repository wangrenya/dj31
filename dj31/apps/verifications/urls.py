from django.urls import path,re_path
from . import  views

app_name = 'verifications'
urlpatterns = [
    path('image_code/<uuid:img_id>/', views.Image_code, name='image_code'),
    re_path('username/(?P<username>\w{5,20})/', views.CheckUsernameView.as_view(), name='check_username'),
    re_path('mobile/(?P<mobile>1[3-9]\d{9})/', views.CheckMobileView.as_view(), name='check_mobile'),
    re_path('sms_code/', views.SmsCodeView.as_view(), name='sms_code'),
]