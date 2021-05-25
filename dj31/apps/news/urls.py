from django.conf import settings
from django.urls import path,re_path


from . import views

app_name= 'news'

urlpatterns = [
    re_path('',views.IndexView.as_view(),name='index'),












]
