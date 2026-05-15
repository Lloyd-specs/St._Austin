from rest_framework import serializers

from .models import InsuranceClaim, Invoice, InvoiceItem, Payment


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = [
            'id', 'invoice', 'description', 'category',
            'quantity', 'unit_price', 'total_price',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PaymentSerializer(serializers.ModelSerializer):
    received_by_name = serializers.CharField(source='received_by.full_name', read_only=True, default=None)

    class Meta:
        model = Payment
        fields = [
            'id', 'invoice', 'amount', 'payment_method',
            'transaction_id', 'status', 'payment_date',
            'received_by', 'received_by_name',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class InsuranceClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceClaim
        fields = [
            'id', 'invoice', 'insurance_provider', 'policy_number',
            'claim_amount', 'approved_amount', 'status',
            'submitted_date', 'response_date',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class InvoiceListSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'patient', 'patient_name',
            'status', 'total', 'insurance_coverage', 'amount_due', 'currency',
            'due_date', 'created_at',
        ]


class InvoiceDetailSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    items = InvoiceItemSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    insurance_claims = InsuranceClaimSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'patient', 'patient_name',
            'consultation', 'status', 'subtotal', 'tax_amount',
            'discount', 'total', 'insurance_coverage', 'amount_due',
            'currency', 'due_date', 'notes',
            'items', 'payments', 'insurance_claims',
            'created_at', 'updated_at', 'created_by',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']
