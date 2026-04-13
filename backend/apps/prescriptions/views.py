import datetime

from django.db.models import Max
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Prescription, PrescriptionItem
from .serializers import PrescriptionItemSerializer, PrescriptionSerializer


def generate_prescription_number():
    year = datetime.date.today().year
    prefix = f'ORD-{year}-'
    last = Prescription.objects.filter(
        prescription_number__startswith=prefix
    ).aggregate(max_num=Max('prescription_number'))['max_num']
    seq = int(last.split('-')[-1]) + 1 if last else 1
    return f'{prefix}{seq:06d}'


class PrescriptionListCreateView(generics.ListCreateAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['patient', 'status', 'prescriber']

    def get_queryset(self):
        return Prescription.objects.select_related(
            'patient', 'prescriber', 'consultation'
        ).prefetch_related('items__medication').filter(is_deleted=False)

    def perform_create(self, serializer):
        serializer.save(
            prescriber=self.request.user,
            created_by=self.request.user,
            prescription_number=generate_prescription_number(),
        )


class PrescriptionDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Prescription.objects.select_related(
            'patient', 'prescriber'
        ).prefetch_related('items__medication').filter(is_deleted=False)


class PrescriptionSignView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            prescription = Prescription.objects.get(pk=pk, is_deleted=False)
        except Prescription.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if prescription.prescriber != request.user:
            return Response(
                {'detail': 'Seul le prescripteur peut signer.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        if prescription.status != 'draft':
            return Response(
                {'detail': 'Seules les ordonnances en brouillon peuvent etre signees.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        prescription.status = 'signed'
        prescription.save(update_fields=['status', 'updated_at', 'sync_version'])
        return Response(PrescriptionSerializer(prescription).data)


class PrescriptionItemCreateView(generics.CreateAPIView):
    serializer_class = PrescriptionItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
