from django.contrib import admin

from .models import EmergencyContact, Patient


class EmergencyContactInline(admin.TabularInline):
    model = EmergencyContact
    extra = 0


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['unique_pid', 'first_name', 'last_name', 'sex', 'phone_primary', 'city']
    search_fields = ['unique_pid', 'first_name', 'last_name', 'national_id']
    list_filter = ['sex', 'blood_type', 'city']
    inlines = [EmergencyContactInline]
