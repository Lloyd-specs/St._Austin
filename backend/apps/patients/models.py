from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class Patient(BaseModel):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    unique_pid = models.CharField(
        max_length=20, unique=True,
        help_text='Format: SIH-YYYY-NNNNNN',
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    national_id = models.CharField(max_length=50, blank=True)
    photo = models.ImageField(upload_to='patients/photos/', blank=True, null=True)
    phone_primary = models.CharField(max_length=20)
    phone_secondary = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, blank=True)
    allergies = models.TextField(blank=True)
    chronic_conditions = models.TextField(blank=True)
    insurance_provider = models.CharField(max_length=200, blank=True)
    insurance_number = models.CharField(max_length=100, blank=True)
    insurance_expiry = models.DateField(null=True, blank=True)

    class Meta(BaseModel.Meta):
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

    def __str__(self):
        return f'{self.unique_pid} - {self.first_name} {self.last_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class EmergencyContact(BaseModel):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='emergency_contacts',
    )
    name = models.CharField(max_length=200)
    relationship = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    class Meta(BaseModel.Meta):
        verbose_name = 'Emergency Contact'
        verbose_name_plural = 'Emergency Contacts'

    def __str__(self):
        return f'{self.name} ({self.relationship}) for {self.patient}'
