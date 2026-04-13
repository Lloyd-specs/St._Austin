from rest_framework import generics, permissions

from .models import Dispensation, Medication
from .serializers import DispensationSerializer, MedicationSerializer


class MedicationListCreateView(generics.ListCreateAPIView):
    serializer_class = MedicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['form', 'category', 'is_active', 'requires_prescription']
    search_fields = ['name', 'generic_name', 'code', 'barcode']

    def get_queryset(self):
        return Medication.objects.filter(is_deleted=False)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class MedicationDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = MedicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Medication.objects.filter(is_deleted=False)


class DispensationListCreateView(generics.ListCreateAPIView):
    serializer_class = DispensationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['prescription', 'medication']

    def get_queryset(self):
        return Dispensation.objects.select_related(
            'medication', 'dispensed_by', 'batch'
        ).filter(is_deleted=False)

    def perform_create(self, serializer):
        dispensation = serializer.save(
            dispensed_by=self.request.user, created_by=self.request.user
        )
        # Decrement batch stock
        batch = dispensation.batch
        batch.quantity_remaining -= dispensation.quantity_dispensed
        batch.save(update_fields=['quantity_remaining', 'updated_at', 'sync_version'])
