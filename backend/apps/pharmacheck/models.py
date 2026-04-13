from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class VerificationLog(BaseModel):
    VERIFICATION_METHOD_CHOICES = [
        ('barcode', 'Code-barres'),
        ('ai_image', 'Analyse IA'),
        ('manual', 'Manuel'),
    ]
    RESULT_CHOICES = [
        ('authentic', 'Authentique'),
        ('suspect', 'Suspect'),
        ('counterfeit', 'Contrefait'),
        ('unknown', 'Inconnu'),
    ]

    medication = models.ForeignKey(
        'pharmacy.Medication', null=True, blank=True, on_delete=models.SET_NULL,
    )
    batch = models.ForeignKey(
        'inventory.Batch', null=True, blank=True, on_delete=models.SET_NULL,
    )
    barcode_data = models.CharField(max_length=255)
    verification_method = models.CharField(max_length=20, choices=VERIFICATION_METHOD_CHOICES)
    result = models.CharField(max_length=20, choices=RESULT_CHOICES)
    confidence_score = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    image = models.ImageField(upload_to='pharmacheck/%Y/%m/', blank=True)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    verified_at = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-verified_at']
        verbose_name = 'Verification PharmaCheck'

    def __str__(self):
        return f'{self.barcode_data} - {self.get_result_display()}'
