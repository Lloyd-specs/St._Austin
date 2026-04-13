from django.contrib import admin

from .models import Batch, StockMovement


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ['medication', 'batch_number', 'quantity_remaining', 'expiry_date', 'is_verified']
    list_filter = ['is_verified', 'expiry_date']


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['batch', 'movement_type', 'quantity', 'movement_date', 'performed_by']
    list_filter = ['movement_type']
