from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from . import views

router = DefaultRouter()
router.register(r'patients', views.PatientViewSet, basename='patient')

patients_router = NestedDefaultRouter(router, r'patients', lookup='patient')
patients_router.register(
    r'emergency-contacts',
    views.EmergencyContactViewSet,
    basename='patient-emergency-contact',
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(patients_router.urls)),
]
