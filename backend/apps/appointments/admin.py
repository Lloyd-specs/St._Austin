from django.contrib import admin

from .models import Appointment, QueueEntry


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'department', 'scheduled_date', 'scheduled_time', 'status']
    list_filter = ['status', 'department', 'scheduled_date']
    search_fields = ['patient__first_name', 'patient__last_name', 'patient__unique_pid']


@admin.register(QueueEntry)
class QueueEntryAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'patient', 'department', 'priority', 'status', 'check_in_time']
    list_filter = ['status', 'priority', 'department']
