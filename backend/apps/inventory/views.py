import datetime

from django.db.models import F, Sum
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Batch, StockMovement
from .serializers import BatchSerializer, StockMovementSerializer


class BatchListCreateView(generics.ListCreateAPIView):
    serializer_class = BatchSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['medication', 'is_verified']

    def get_queryset(self):
        return Batch.objects.select_related('medication').filter(is_deleted=False)

    def perform_create(self, serializer):
        batch = serializer.save(created_by=self.request.user)
        StockMovement.objects.create(
            batch=batch,
            movement_type='entry',
            quantity=batch.quantity_received,
            reason='Reception initiale',
            performed_by=self.request.user,
            created_by=self.request.user,
        )


class BatchDetailView(generics.RetrieveAPIView):
    serializer_class = BatchSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Batch.objects.filter(is_deleted=False)


class StockMovementListCreateView(generics.ListCreateAPIView):
    serializer_class = StockMovementSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['batch', 'movement_type']

    def get_queryset(self):
        return StockMovement.objects.select_related('batch__medication', 'performed_by').filter(is_deleted=False)

    def perform_create(self, serializer):
        movement = serializer.save(performed_by=self.request.user, created_by=self.request.user)
        batch = movement.batch
        if movement.movement_type in ('entry', 'return'):
            batch.quantity_remaining = F('quantity_remaining') + abs(movement.quantity)
        else:
            batch.quantity_remaining = F('quantity_remaining') - abs(movement.quantity)
        batch.save(update_fields=['quantity_remaining', 'updated_at', 'sync_version'])


class InventoryAlertsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = datetime.date.today()
        days_30 = today + datetime.timedelta(days=30)

        expiring = Batch.objects.filter(
            expiry_date__lte=days_30, expiry_date__gt=today,
            quantity_remaining__gt=0, is_deleted=False,
        ).select_related('medication').values(
            'id', 'medication__name', 'batch_number', 'expiry_date', 'quantity_remaining',
        )

        from apps.pharmacy.models import Medication
        low_stock = Medication.objects.filter(
            is_active=True, is_deleted=False,
        ).annotate(
            total_stock=Sum('batches__quantity_remaining')
        ).filter(total_stock__lt=F('reorder_level')).values(
            'id', 'name', 'reorder_level', 'total_stock',
        )

        return Response({
            'expiring_soon': list(expiring),
            'low_stock': list(low_stock),
        })
