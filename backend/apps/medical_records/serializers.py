from rest_framework import serializers

from .models import Consultation, MedicalDocument, VitalSign


class VitalSignSerializer(serializers.ModelSerializer):
    recorded_by_name = serializers.CharField(source='recorded_by.full_name', read_only=True)

    class Meta:
        model = VitalSign
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'recorded_at']


class MedicalDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalDocument
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class ConsultationSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)
    patient_name = serializers.SerializerMethodField()
    vitals = VitalSignSerializer(many=True, read_only=True)

    class Meta:
        model = Consultation
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'date']

    def get_patient_name(self, obj):
        return f'{obj.patient.first_name} {obj.patient.last_name}'
