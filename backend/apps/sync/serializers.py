from rest_framework import serializers

from .models import ConflictRecord, SyncLog


class ConflictRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConflictRecord
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class SyncLogSerializer(serializers.ModelSerializer):
    conflicts = ConflictRecordSerializer(many=True, read_only=True)

    class Meta:
        model = SyncLog
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'synced_at']
