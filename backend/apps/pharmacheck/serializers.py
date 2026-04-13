from rest_framework import serializers

from .models import VerificationLog


class VerificationLogSerializer(serializers.ModelSerializer):
    result_display = serializers.CharField(source='get_result_display', read_only=True)
    medication_name = serializers.CharField(source='medication.name', read_only=True, default=None)

    class Meta:
        model = VerificationLog
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'verified_at']
