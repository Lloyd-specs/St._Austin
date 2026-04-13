from django.urls import path

from . import views

urlpatterns = [
    path('medications/', views.MedicationListCreateView.as_view(), name='medication_list'),
    path('medications/<uuid:pk>/', views.MedicationDetailView.as_view(), name='medication_detail'),
    path('dispensations/', views.DispensationListCreateView.as_view(), name='dispensation_list'),
]
