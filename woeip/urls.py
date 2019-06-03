from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .apps.air_quality import views
from .apps.core.views import health

urlpatterns = [
    path('', views.Upload.as_view(), name='upload'),
    path('delete/<int:document_id>', views.delete, name='delete'),
    path('submit/', views.submit, name='submit'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('health/', health, name='health'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
