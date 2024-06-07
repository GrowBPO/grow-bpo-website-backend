from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 


urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('hidden/grow/admin/', admin.site.urls),
    path('api/auth/', include("login.urls")),
    path('api/bi/', include("bi_report.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

