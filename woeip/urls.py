from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from .apps.air_quality.views import Upload
from .apps.core.views import health

urlpatterns = [
    path('', Upload.as_view(), name='upload'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('health/', health, name='health'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
