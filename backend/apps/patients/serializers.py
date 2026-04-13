from rest_framework import serializers

from .models import EmergencyContact, Patient


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = [
            'id', 'patient', 'name', 'relationship', 'phone',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PatientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            'id', 'unique_pid', 'first_name', 'last_name',
            'date_of_birth', 'sex', 'phone_primary', 'city',
            'insurance_provider', 'created_at',
        ]


class PatientDetailSerializer(serializers.ModelSerializer):
    emergency_contacts = EmergencyContactSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id', 'unique_pid', 'first_name', 'last_name',
            'date_of_birth', 'sex', 'national_id', 'photo',
            'phone_primary', 'phone_secondary', 'email',
            'address', 'city', 'region', 'blood_type',
            'allergies', 'chronic_conditions',
            'insurance_provider', 'insurance_number', 'insurance_expiry',
            'emergency_contacts',
            'created_at', 'updated_at', 'created_by',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']
