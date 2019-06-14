from django.contrib import admin
from django.urls import include, path
# TODO: Document adding development specific media url
from django.conf import settings
from django.conf.urls.static import static

from .apps.air_quality import views
from .apps.core.views import health

# TODO: Document structure of the URLS. And names of pages/templates. Current format doesn't effectivly communicate function of pages
# TODO: format review_upload url so that it can be accessed 
urlpatterns = [
    path('', views.Upload.as_view(), name='upload'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('health/', health, name='health'),
    path('view_session_data/', views.ViewSessionData.as_view(), name='view_session_data'),
    path('review_upload/(?P<sessionData_id>\d+)/', views.ReviewUpload.as_view(), name='review_upload')
]

# Document Development access to static files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
