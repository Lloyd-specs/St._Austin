from rest_framework import serializers

from .models import Appointment, QueueEntry


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'patient_name', 'doctor', 'doctor_name',
            'department', 'scheduled_date', 'scheduled_time',
            'duration_minutes', 'status', 'reason', 'notes',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class QueueEntrySerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    served_by_name = serializers.CharField(source='served_by.full_name', read_only=True, default=None)

    class Meta:
        model = QueueEntry
        fields = [
            'id', 'patient', 'patient_name', 'appointment',
            'department', 'priority', 'ticket_number', 'status',
            'check_in_time', 'called_time', 'served_by', 'served_by_name',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'check_in_time', 'created_at', 'updated_at']
