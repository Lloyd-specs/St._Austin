from rest_framework import generics, permissions

from .models import Consultation, MedicalDocument, VitalSign
from .serializers import ConsultationSerializer, MedicalDocumentSerializer, VitalSignSerializer


class ConsultationListCreateView(generics.ListCreateAPIView):
    serializer_class = ConsultationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['patient', 'doctor', 'is_confidential']
    search_fields = ['chief_complaint', 'assessment']

    def get_queryset(self):
        return Consultation.objects.select_related(
            'patient', 'doctor', 'appointment'
        ).prefetch_related('vitals').filter(is_deleted=False)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, doctor=self.request.user)


class ConsultationDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ConsultationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Consultation.objects.select_related(
            'patient', 'doctor'
        ).prefetch_related('vitals').filter(is_deleted=False)


class VitalSignListCreateView(generics.ListCreateAPIView):
    serializer_class = VitalSignSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['patient', 'consultation']

    def get_queryset(self):
        return VitalSign.objects.select_related('patient', 'recorded_by').filter(is_deleted=False)

    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user, created_by=self.request.user)


class VitalSignDetailView(generics.RetrieveAPIView):
    serializer_class = VitalSignSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = VitalSign.objects.filter(is_deleted=False)


class PatientVitalsView(generics.ListAPIView):
    serializer_class = VitalSignSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VitalSign.objects.filter(
            patient_id=self.kwargs['patient_id'], is_deleted=False
        ).select_related('recorded_by')


class MedicalDocumentListCreateView(generics.ListCreateAPIView):
    serializer_class = MedicalDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['patient', 'document_type']

    def get_queryset(self):
        return MedicalDocument.objects.filter(is_deleted=False)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class MedicalDocumentDetailView(generics.RetrieveAPIView):
    serializer_class = MedicalDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = MedicalDocument.objects.filter(is_deleted=False)
