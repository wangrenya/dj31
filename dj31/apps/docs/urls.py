from .import views
from django.urls import path,re_path,include



from dj31.settings import dev

app_name = 'docs'
urlpatterns = [
    path('<int:d_id>/', views.load, name='d_load'),
    re_path('',views.docs,name='d_doc'),

]
