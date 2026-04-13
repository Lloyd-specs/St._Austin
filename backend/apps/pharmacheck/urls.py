from django.urls import path

from . import views

urlpatterns = [
    path('pharmacheck/verify-barcode/', views.VerifyBarcodeView.as_view(), name='pharmacheck_barcode'),
    path('pharmacheck/verify-image/', views.VerifyImageView.as_view(), name='pharmacheck_image'),
    path('pharmacheck/logs/', views.VerificationLogListView.as_view(), name='pharmacheck_logs'),
    path('pharmacheck/logs/<uuid:pk>/', views.VerificationLogDetailView.as_view(), name='pharmacheck_log_detail'),
]
