from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'appointments', views.AppointmentViewSet, basename='appointment')
router.register(r'queue', views.QueueEntryViewSet, basename='queue-entry')

urlpatterns = [
    path('', include(router.urls)),
]
