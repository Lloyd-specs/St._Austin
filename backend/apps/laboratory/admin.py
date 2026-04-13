from django.contrib import admin

from .models import ImagingOrder, LabOrder, LabResult, LabTest


@admin.register(LabOrder)
class LabOrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'patient', 'status', 'priority', 'ordered_date']
    list_filter = ['status', 'priority']


@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ['test_code', 'test_name', 'category', 'order']


@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display = ['test', 'value', 'is_abnormal', 'validated_by']


@admin.register(ImagingOrder)
class ImagingOrderAdmin(admin.ModelAdmin):
    list_display = ['modality', 'body_part', 'patient', 'status']
    list_filter = ['modality', 'status']
