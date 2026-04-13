from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import InsuranceClaim, Invoice, InvoiceItem, Payment
from .serializers import (
    InsuranceClaimSerializer,
    InvoiceDetailSerializer,
    InvoiceItemSerializer,
    InvoiceListSerializer,
    PaymentSerializer,
)


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.filter(is_deleted=False).select_related('patient', 'consultation')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'currency', 'patient']
    search_fields = ['invoice_number', 'patient__first_name', 'patient__last_name']
    ordering_fields = ['created_at', 'due_date', 'total']

    def get_serializer_class(self):
        if self.action == 'list':
            return InvoiceListSerializer
        return InvoiceDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class InvoiceItemViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InvoiceItem.objects.filter(
            invoice_id=self.kwargs.get('invoice_pk'),
            is_deleted=False,
        )

    def perform_create(self, serializer):
        serializer.save(
            invoice_id=self.kwargs['invoice_pk'],
            created_by=self.request.user,
        )


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.filter(is_deleted=False).select_related('invoice', 'received_by')
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_method', 'invoice']
    ordering_fields = ['payment_date', 'amount']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class InsuranceClaimViewSet(viewsets.ModelViewSet):
    queryset = InsuranceClaim.objects.filter(is_deleted=False).select_related('invoice')
    serializer_class = InsuranceClaimSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'insurance_provider', 'invoice']
    ordering_fields = ['submitted_date', 'claim_amount']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
