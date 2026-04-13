from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class LabOrder(BaseModel):
    STATUS_CHOICES = [
        ('ordered', 'Commande'),
        ('in_progress', 'En cours'),
        ('completed', 'Termine'),
        ('cancelled', 'Annule'),
    ]
    PRIORITY_CHOICES = [
        ('routine', 'Routine'),
        ('urgent', 'Urgent'),
        ('stat', 'STAT'),
    ]

    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='lab_orders')
    consultation = models.ForeignKey('medical_records.Consultation', on_delete=models.CASCADE)
    ordered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lab_orders_placed')
    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ordered')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='routine')
    ordered_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-ordered_date']
        verbose_name = 'Demande labo'

    def __str__(self):
        return self.order_number


class LabTest(BaseModel):
    order = models.ForeignKey(LabOrder, on_delete=models.CASCADE, related_name='tests')
    test_name = models.CharField(max_length=200)
    test_code = models.CharField(max_length=20)
    category = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.test_code} - {self.test_name}'


class LabResult(BaseModel):
    test = models.OneToOneField(LabTest, on_delete=models.CASCADE, related_name='result')
    value = models.CharField(max_length=200)
    unit = models.CharField(max_length=50, blank=True)
    reference_range = models.CharField(max_length=100, blank=True)
    is_abnormal = models.BooleanField(default=False)
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
        related_name='validated_lab_results',
    )
    result_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Resultat labo'

    def __str__(self):
        return f'{self.test} = {self.value}'


class ImagingOrder(BaseModel):
    MODALITY_CHOICES = [
        ('xray', 'Radiographie'),
        ('ultrasound', 'Echographie'),
        ('ct', 'Scanner'),
        ('mri', 'IRM'),
    ]

    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='imaging_orders')
    consultation = models.ForeignKey('medical_records.Consultation', on_delete=models.CASCADE)
    ordered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    modality = models.CharField(max_length=30, choices=MODALITY_CHOICES)
    body_part = models.CharField(max_length=100)
    clinical_indication = models.TextField()
    status = models.CharField(max_length=20, default='ordered')
    report = models.TextField(blank=True)
    report_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='imaging_reports',
    )
    images = models.FileField(upload_to='imaging/%Y/%m/', blank=True)

    class Meta:
        verbose_name = 'Demande imagerie'

    def __str__(self):
        return f'{self.get_modality_display()} - {self.body_part}'
