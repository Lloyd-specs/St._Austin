from django.urls import path

from . import views

urlpatterns = [
    path('prescriptions/', views.PrescriptionListCreateView.as_view(), name='prescription_list'),
    path('prescriptions/<uuid:pk>/', views.PrescriptionDetailView.as_view(), name='prescription_detail'),
    path('prescriptions/<uuid:pk>/sign/', views.PrescriptionSignView.as_view(), name='prescription_sign'),
    path('prescriptions/<uuid:pk>/items/', views.PrescriptionItemCreateView.as_view(), name='prescription_item_create'),
]
