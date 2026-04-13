from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class Invoice(BaseModel):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('partially_paid', 'Partially Paid'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]

    invoice_number = models.CharField(
        max_length=20, unique=True,
        help_text='Format: FACT-YYYY-NNNNNN',
    )
    patient = models.ForeignKey(
        'patients.Patient', on_delete=models.CASCADE, related_name='invoices',
    )
    consultation = models.ForeignKey(
        'medical_records.Consultation', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='invoices',
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    insurance_coverage = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount_due = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='XAF')
    due_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'

    def __str__(self):
        return f'{self.invoice_number} - {self.patient}'


class InvoiceItem(BaseModel):
    CATEGORY_CHOICES = [
        ('consultation', 'Consultation'),
        ('lab', 'Laboratory'),
        ('imaging', 'Imaging'),
        ('medication', 'Medication'),
        ('procedure', 'Procedure'),
        ('room', 'Room'),
    ]

    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name='items',
    )
    description = models.CharField(max_length=300)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta(BaseModel.Meta):
        verbose_name = 'Invoice Item'
        verbose_name_plural = 'Invoice Items'

    def __str__(self):
        return f'{self.description} ({self.invoice.invoice_number})'


class Payment(BaseModel):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('mtn_momo', 'MTN Mobile Money'),
        ('orange_money', 'Orange Money'),
        ('insurance', 'Insurance'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name='payments',
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField()
    received_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='received_payments',
    )

    class Meta(BaseModel.Meta):
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return f'Payment {self.amount} {self.invoice.currency} for {self.invoice.invoice_number}'


class InsuranceClaim(BaseModel):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
    ]

    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name='insurance_claims',
    )
    insurance_provider = models.CharField(max_length=200)
    policy_number = models.CharField(max_length=100)
    claim_amount = models.DecimalField(max_digits=12, decimal_places=2)
    approved_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    submitted_date = models.DateField()
    response_date = models.DateField(null=True, blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = 'Insurance Claim'
        verbose_name_plural = 'Insurance Claims'

    def __str__(self):
        return f'Claim {self.policy_number} - {self.invoice.invoice_number}'
