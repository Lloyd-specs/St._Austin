from django.contrib import admin

from .models import Consultation, MedicalDocument, VitalSign


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'date', 'chief_complaint']
    list_filter = ['date', 'is_confidential']
    search_fields = ['patient__first_name', 'patient__last_name', 'chief_complaint']


@admin.register(VitalSign)
class VitalSignAdmin(admin.ModelAdmin):
    list_display = ['patient', 'recorded_at', 'temperature', 'heart_rate']
    list_filter = ['recorded_at']


@admin.register(MedicalDocument)
class MedicalDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'patient', 'document_type', 'created_at']
    list_filter = ['document_type']
