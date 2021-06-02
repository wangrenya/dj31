from .import views
from django.urls import path,re_path,include
from django.views.static import serve


from dj31.settings import dev
from django.conf import settings
app_name = 'courses'
urlpatterns = [
    path('video/', views.video, name='video'),
    path('', views.videos, name='course'),
    path('<int:c_id>/', views.Course_detail.as_view(), name='c_detail')

    # re_path('media/(?P<path>.*)/', serve, {'document_root': dev.MEDIA_ROOT}),

]
