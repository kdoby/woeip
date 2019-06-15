# TODO: Document adding development specific media url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .apps.air_quality import views
from .apps.core.views import health

# TODO: Document structure of the URLS. And names of pages/templates.
# Current format doesn't effectivly communicate function of pages
urlpatterns = [
    path('', views.Upload.as_view(), name='upload'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('health/', health, name='health'),
    path('confirm/<int:session_data_id>/', views.Confirm.as_view(), name='confirm'),
    path('view/', views.ViewSessionData.as_view(), name='view')
]

# Document Development access to static files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
