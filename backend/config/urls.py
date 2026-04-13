from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    # API v1
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/', include('apps.patients.urls')),
    path('api/v1/', include('apps.appointments.urls')),
    path('api/v1/', include('apps.billing.urls')),
    path('api/v1/', include('apps.medical_records.urls')),
    path('api/v1/', include('apps.prescriptions.urls')),
    path('api/v1/', include('apps.laboratory.urls')),
    path('api/v1/', include('apps.pharmacy.urls')),
    path('api/v1/', include('apps.inventory.urls')),
    path('api/v1/', include('apps.pharmacheck.urls')),
    path('api/v1/', include('apps.dashboard.urls')),
    path('api/v1/', include('apps.sync.urls')),
    # API Schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
