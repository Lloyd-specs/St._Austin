from django.urls import path

from . import views

urlpatterns = [
    path('consultations/', views.ConsultationListCreateView.as_view(), name='consultation_list'),
    path('consultations/<uuid:pk>/', views.ConsultationDetailView.as_view(), name='consultation_detail'),
    path('vitals/', views.VitalSignListCreateView.as_view(), name='vital_list'),
    path('vitals/<uuid:pk>/', views.VitalSignDetailView.as_view(), name='vital_detail'),
    path('patients/<uuid:patient_id>/vitals/', views.PatientVitalsView.as_view(), name='patient_vitals'),
    path('documents/', views.MedicalDocumentListCreateView.as_view(), name='document_list'),
    path('documents/<uuid:pk>/', views.MedicalDocumentDetailView.as_view(), name='document_detail'),
]
