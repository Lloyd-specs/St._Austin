from django.contrib import admin

from .models import VerificationLog


@admin.register(VerificationLog)
class VerificationLogAdmin(admin.ModelAdmin):
    list_display = ['barcode_data', 'verification_method', 'result', 'confidence_score', 'verified_at']
    list_filter = ['result', 'verification_method']
