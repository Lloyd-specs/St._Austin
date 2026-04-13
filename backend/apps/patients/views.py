from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import EmergencyContact, Patient
from .serializers import (
    EmergencyContactSerializer,
    PatientDetailSerializer,
    PatientListSerializer,
)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.filter(is_deleted=False)
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['unique_pid', 'first_name', 'last_name', 'phone_primary', 'national_id']
    filterset_fields = ['sex', 'city', 'blood_type', 'insurance_provider']
    ordering_fields = ['created_at', 'last_name', 'unique_pid']

    def get_serializer_class(self):
        if self.action == 'list':
            return PatientListSerializer
        return PatientDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class EmergencyContactViewSet(viewsets.ModelViewSet):
    serializer_class = EmergencyContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EmergencyContact.objects.filter(
            patient_id=self.kwargs['patient_pk'],
            is_deleted=False,
        )

    def perform_create(self, serializer):
        serializer.save(
            patient_id=self.kwargs['patient_pk'],
            created_by=self.request.user,
        )
