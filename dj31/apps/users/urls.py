"""dj31 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,re_path,include
from . import  views

app_name='users'
urlpatterns = [
    re_path('register/',views.RegisView.as_view(),name='register'),
    re_path('login/',views.LoginView.as_view(),name='login'),
    re_path('logout/',views.LogoutView.as_view(),name='logout'),
    re_path('check_pwd/',views.CheckPwd.as_view(),name='check_pwd'),
    re_path('c_pwd/',views.Passwd.as_view(),name='c_pwd'),
]
