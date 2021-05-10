from django.urls import path,re_path
from . import  views

app_name = 'verifications'
urlpatterns = [

    path('image_code/<uuid:img_id>/', views.Image_code, name='image_code'),
    re_path('username/(?P<username>\w{5,20})/', views.CheckUsernameView.as_view(), name='check_username'),
]