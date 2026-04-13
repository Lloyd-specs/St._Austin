from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Appointment, QueueEntry
from .serializers import AppointmentSerializer, QueueEntrySerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.filter(is_deleted=False).select_related('patient', 'doctor')
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'department', 'doctor', 'scheduled_date']
    search_fields = ['patient__first_name', 'patient__last_name', 'patient__unique_pid']
    ordering_fields = ['scheduled_date', 'scheduled_time', 'created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class QueueEntryViewSet(viewsets.ModelViewSet):
    queryset = QueueEntry.objects.filter(is_deleted=False).select_related(
        'patient', 'appointment', 'served_by',
    )
    serializer_class = QueueEntrySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'department', 'priority']
    ordering_fields = ['priority', 'check_in_time']
    ordering = ['-priority', 'check_in_time']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
