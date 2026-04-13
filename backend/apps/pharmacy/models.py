from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class Medication(BaseModel):
    FORM_CHOICES = [
        ('tablet', 'Comprime'),
        ('capsule', 'Gelule'),
        ('syrup', 'Sirop'),
        ('injection', 'Injectable'),
        ('cream', 'Creme'),
        ('drops', 'Gouttes'),
        ('inhaler', 'Inhalateur'),
        ('suppository', 'Suppositoire'),
    ]

    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255, db_index=True)
    generic_name = models.CharField(max_length=255, db_index=True)
    form = models.CharField(max_length=50, choices=FORM_CHOICES)
    strength = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=100)
    requires_prescription = models.BooleanField(default=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    reorder_level = models.IntegerField(default=10)
    barcode = models.CharField(max_length=50, blank=True, db_index=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Medicament'

    def __str__(self):
        return f'{self.name} {self.strength} ({self.get_form_display()})'


class Dispensation(BaseModel):
    prescription = models.ForeignKey(
        'prescriptions.Prescription', on_delete=models.CASCADE, related_name='dispensations'
    )
    prescription_item = models.ForeignKey(
        'prescriptions.PrescriptionItem', on_delete=models.CASCADE,
    )
    dispensed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        limit_choices_to={'role__name': 'pharmacien'},
    )
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    batch = models.ForeignKey('inventory.Batch', on_delete=models.CASCADE)
    quantity_dispensed = models.IntegerField()
    dispensed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-dispensed_at']
        verbose_name = 'Dispensation'

    def __str__(self):
        return f'{self.medication} x{self.quantity_dispensed}'
