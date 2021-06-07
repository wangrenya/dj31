from .import views
from django.urls import path,re_path,include




app_name = 'admin'
urlpatterns = [
  re_path('',views.admin,name='admin')

]
