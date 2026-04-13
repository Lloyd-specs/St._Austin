from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'invoices', views.InvoiceViewSet, basename='invoice')
router.register(r'payments', views.PaymentViewSet, basename='payment')
router.register(r'insurance-claims', views.InsuranceClaimViewSet, basename='insurance-claim')

urlpatterns = [
    path('', include(router.urls)),
]
