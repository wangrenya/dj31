from django.urls import path,re_path,include
from django.views.static import serve


from dj31.settings import dev
from django.conf import settings
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('user/',include('users.urls')),
    path('',include('verifications.urls')),
    path('',include('qauth.urls')),
    path('',include('news.urls')),
    path('courses/',include('courses.urls')),
    path('docs/',include('docs.urls')),
    # re_path('media/(?P<path>.*)/', serve, {'document_root': dev.MEDIA_ROOT}),

]
