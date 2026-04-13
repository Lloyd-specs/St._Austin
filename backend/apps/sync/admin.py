from django.contrib import admin

from .models import ConflictRecord, SyncLog


@admin.register(SyncLog)
class SyncLogAdmin(admin.ModelAdmin):
    list_display = ['entity_type', 'entity_id', 'action', 'status', 'device_id', 'synced_at']
    list_filter = ['status', 'sync_type', 'entity_type']


@admin.register(ConflictRecord)
class ConflictRecordAdmin(admin.ModelAdmin):
    list_display = ['sync_log', 'field_name', 'resolved_at']
