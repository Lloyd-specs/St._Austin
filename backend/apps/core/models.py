import uuid

from django.conf import settings
from django.db import models


class BaseModel(models.Model):
    """Base model with UUID primary key, audit fields, and sync support."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_created',
    )
    is_deleted = models.BooleanField(default=False)
    sync_version = models.BigIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self._state.adding:
            self.sync_version += 1
        super().save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.save(update_fields=['is_deleted', 'updated_at', 'sync_version'])
