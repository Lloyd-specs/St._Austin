from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class Batch(BaseModel):
    medication = models.ForeignKey('pharmacy.Medication', on_delete=models.CASCADE, related_name='batches')
    batch_number = models.CharField(max_length=50)
    quantity_received = models.IntegerField()
    quantity_remaining = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.CharField(max_length=200)
    received_date = models.DateField()
    expiry_date = models.DateField(db_index=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ['expiry_date']
        verbose_name = 'Lot'
        indexes = [
            models.Index(fields=['medication', 'expiry_date']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity_remaining__gte=0),
                name='non_negative_stock',
            ),
        ]

    def __str__(self):
        return f'{self.medication.name} - Lot {self.batch_number}'


class StockMovement(BaseModel):
    MOVEMENT_TYPE_CHOICES = [
        ('entry', 'Entree'),
        ('exit', 'Sortie'),
        ('adjustment', 'Ajustement'),
        ('return', 'Retour'),
        ('expired', 'Perime'),
        ('damaged', 'Endommage'),
    ]

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES)
    quantity = models.IntegerField()
    reason = models.TextField(blank=True)
    reference = models.CharField(max_length=100, blank=True)
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    movement_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-movement_date']
        verbose_name = 'Mouvement stock'

    def __str__(self):
        return f'{self.get_movement_type_display()} - {self.batch} ({self.quantity})'
