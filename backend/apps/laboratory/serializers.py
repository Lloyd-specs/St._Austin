from rest_framework import serializers

from .models import ImagingOrder, LabOrder, LabResult, LabTest


class LabResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabResult
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'result_date']


class LabTestSerializer(serializers.ModelSerializer):
    result = LabResultSerializer(read_only=True)

    class Meta:
        model = LabTest
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class LabOrderSerializer(serializers.ModelSerializer):
    tests = LabTestSerializer(many=True, read_only=True)
    ordered_by_name = serializers.CharField(source='ordered_by.full_name', read_only=True)

    class Meta:
        model = LabOrder
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'ordered_date', 'order_number']


class ImagingOrderSerializer(serializers.ModelSerializer):
    ordered_by_name = serializers.CharField(source='ordered_by.full_name', read_only=True)

    class Meta:
        model = ImagingOrder
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
