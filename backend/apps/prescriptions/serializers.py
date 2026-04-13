from rest_framework import serializers

from .models import Prescription, PrescriptionItem


class PrescriptionItemSerializer(serializers.ModelSerializer):
    medication_name = serializers.CharField(source='medication.name', read_only=True)

    class Meta:
        model = PrescriptionItem
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class PrescriptionSerializer(serializers.ModelSerializer):
    items = PrescriptionItemSerializer(many=True, read_only=True)
    prescriber_name = serializers.CharField(source='prescriber.full_name', read_only=True)
    patient_name = serializers.SerializerMethodField()

    class Meta:
        model = Prescription
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'prescribed_date', 'prescription_number']

    def get_patient_name(self, obj):
        return f'{obj.patient.first_name} {obj.patient.last_name}'
