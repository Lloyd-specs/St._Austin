from django.contrib import admin

from .models import Dispensation, Medication


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'generic_name', 'form', 'strength', 'unit_price', 'is_active']
    list_filter = ['form', 'category', 'is_active']
    search_fields = ['name', 'generic_name', 'code']


@admin.register(Dispensation)
class DispensationAdmin(admin.ModelAdmin):
    list_display = ['medication', 'quantity_dispensed', 'dispensed_by', 'dispensed_at']
