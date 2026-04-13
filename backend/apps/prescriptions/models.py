from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class Prescription(BaseModel):
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('signed', 'Signee'),
        ('partially_dispensed', 'Partiellement dispensee'),
        ('dispensed', 'Dispensee'),
        ('cancelled', 'Annulee'),
    ]

    prescription_number = models.CharField(max_length=20, unique=True)
    patient = models.ForeignKey(
        'patients.Patient', on_delete=models.CASCADE, related_name='prescriptions'
    )
    consultation = models.ForeignKey(
        'medical_records.Consultation', on_delete=models.CASCADE, related_name='prescriptions'
    )
    prescriber = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='prescriptions_written',
        limit_choices_to={'role__name': 'medecin'},
    )
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='draft')
    prescribed_date = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateField()
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-prescribed_date']
        verbose_name = 'Ordonnance'

    def __str__(self):
        return f'{self.prescription_number} - {self.patient}'


class PrescriptionItem(BaseModel):
    ROUTE_CHOICES = [
        ('oral', 'Oral'),
        ('iv', 'Intraveineux'),
        ('im', 'Intramusculaire'),
        ('topical', 'Topique'),
        ('sublingual', 'Sublingual'),
        ('rectal', 'Rectal'),
        ('inhalation', 'Inhalation'),
    ]

    prescription = models.ForeignKey(
        Prescription, on_delete=models.CASCADE, related_name='items'
    )
    medication = models.ForeignKey('pharmacy.Medication', on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    quantity = models.IntegerField()
    route = models.CharField(max_length=50, choices=ROUTE_CHOICES, default='oral')
    instructions = models.TextField(blank=True)
    is_substitutable = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Ligne ordonnance'

    def __str__(self):
        return f'{self.medication} - {self.dosage}'
