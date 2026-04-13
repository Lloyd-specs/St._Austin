import uuid

from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class SyncLog(BaseModel):
    SYNC_TYPE_CHOICES = [('push', 'Push'), ('pull', 'Pull')]
    ACTION_CHOICES = [('create', 'Create'), ('update', 'Update'), ('delete', 'Delete')]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('applied', 'Applied'),
        ('conflict', 'Conflict'),
        ('rejected', 'Rejected'),
    ]

    device_id = models.CharField(max_length=100, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sync_type = models.CharField(max_length=10, choices=SYNC_TYPE_CHOICES)
    entity_type = models.CharField(max_length=50)
    entity_id = models.UUIDField()
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    payload = models.JSONField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    conflict_resolved_by = models.CharField(max_length=20, blank=True)
    synced_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-synced_at']
        verbose_name = 'Log synchronisation'

    def __str__(self):
        return f'{self.sync_type} {self.entity_type}:{self.entity_id} [{self.status}]'


class ConflictRecord(BaseModel):
    sync_log = models.ForeignKey(SyncLog, on_delete=models.CASCADE, related_name='conflicts')
    field_name = models.CharField(max_length=100)
    server_value = models.TextField()
    client_value = models.TextField()
    resolved_value = models.TextField(blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Conflit sync'

    def __str__(self):
        return f'{self.sync_log} - {self.field_name}'
