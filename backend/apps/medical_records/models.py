from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class Consultation(BaseModel):
    patient = models.ForeignKey(
        'patients.Patient', on_delete=models.CASCADE, related_name='consultations'
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='consultations', limit_choices_to={'role__name': 'medecin'},
    )
    appointment = models.ForeignKey(
        'appointments.Appointment', null=True, blank=True, on_delete=models.SET_NULL,
    )
    date = models.DateTimeField(auto_now_add=True)
    chief_complaint = models.TextField(verbose_name='Motif de consultation')
    history_present_illness = models.TextField(blank=True)
    physical_examination = models.TextField(blank=True)
    assessment = models.TextField(blank=True, verbose_name='Diagnostic')
    plan = models.TextField(blank=True, verbose_name='Plan de traitement')
    follow_up_date = models.DateField(null=True, blank=True)
    is_confidential = models.BooleanField(default=False)
    diagnosis_codes = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Consultation'

    def __str__(self):
        return f'Consultation {self.patient} - {self.date:%d/%m/%Y}'


class VitalSign(BaseModel):
    patient = models.ForeignKey(
        'patients.Patient', on_delete=models.CASCADE, related_name='vitals'
    )
    consultation = models.ForeignKey(
        Consultation, null=True, blank=True, on_delete=models.SET_NULL, related_name='vitals',
    )
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
    )
    recorded_at = models.DateTimeField(auto_now_add=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    blood_pressure_systolic = models.IntegerField(null=True, blank=True)
    blood_pressure_diastolic = models.IntegerField(null=True, blank=True)
    heart_rate = models.IntegerField(null=True, blank=True)
    respiratory_rate = models.IntegerField(null=True, blank=True)
    oxygen_saturation = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-recorded_at']
        verbose_name = 'Constantes Vitales'

    def __str__(self):
        return f'Vitals {self.patient} - {self.recorded_at:%d/%m/%Y %H:%M}'


class MedicalDocument(BaseModel):
    DOCUMENT_TYPE_CHOICES = [
        ('lab_result', 'Resultat labo'),
        ('imaging', 'Imagerie'),
        ('report', 'Rapport'),
        ('certificate', 'Certificat'),
        ('other', 'Autre'),
    ]

    patient = models.ForeignKey(
        'patients.Patient', on_delete=models.CASCADE, related_name='documents'
    )
    consultation = models.ForeignKey(
        Consultation, null=True, blank=True, on_delete=models.SET_NULL,
    )
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='medical_docs/%Y/%m/')
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Document Medical'

    def __str__(self):
        return f'{self.title} - {self.patient}'
