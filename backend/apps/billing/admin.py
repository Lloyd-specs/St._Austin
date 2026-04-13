from django.contrib import admin

from .models import InsuranceClaim, Invoice, InvoiceItem, Payment


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'patient', 'status', 'total', 'amount_due', 'currency', 'due_date']
    list_filter = ['status', 'currency']
    search_fields = ['invoice_number', 'patient__first_name', 'patient__last_name']
    inlines = [InvoiceItemInline, PaymentInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'amount', 'payment_method', 'status', 'payment_date']
    list_filter = ['status', 'payment_method']


@admin.register(InsuranceClaim)
class InsuranceClaimAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'insurance_provider', 'claim_amount', 'approved_amount', 'status']
    list_filter = ['status', 'insurance_provider']
