from rest_framework import serializers

from .models import Dispensation, Medication


class MedicationSerializer(serializers.ModelSerializer):
    form_display = serializers.CharField(source='get_form_display', read_only=True)

    class Meta:
        model = Medication
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class DispensationSerializer(serializers.ModelSerializer):
    medication_name = serializers.CharField(source='medication.name', read_only=True)
    dispensed_by_name = serializers.CharField(source='dispensed_by.full_name', read_only=True)

    class Meta:
        model = Dispensation
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'dispensed_at']
