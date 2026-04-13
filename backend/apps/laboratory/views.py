from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ImagingOrder, LabOrder, LabResult, LabTest
from .serializers import ImagingOrderSerializer, LabOrderSerializer, LabResultSerializer


class LabOrderListCreateView(generics.ListCreateAPIView):
    serializer_class = LabOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['patient', 'status', 'priority']

    def get_queryset(self):
        return LabOrder.objects.select_related(
            'patient', 'ordered_by'
        ).prefetch_related('tests__result').filter(is_deleted=False)

    def perform_create(self, serializer):
        import datetime
        from django.db.models import Max
        year = datetime.date.today().year
        prefix = f'LAB-{year}-'
        last = LabOrder.objects.filter(
            order_number__startswith=prefix
        ).aggregate(m=Max('order_number'))['m']
        seq = int(last.split('-')[-1]) + 1 if last else 1
        serializer.save(
            ordered_by=self.request.user,
            created_by=self.request.user,
            order_number=f'{prefix}{seq:06d}',
        )


class LabOrderDetailView(generics.RetrieveAPIView):
    serializer_class = LabOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = LabOrder.objects.filter(is_deleted=False)


class LabResultCreateView(generics.CreateAPIView):
    serializer_class = LabResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(performed_by=self.request.user, created_by=self.request.user)


class LabResultUpdateView(generics.UpdateAPIView):
    serializer_class = LabResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = LabResult.objects.filter(is_deleted=False)


class LabResultValidateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            result = LabResult.objects.get(pk=pk, is_deleted=False)
        except LabResult.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        result.validated_by = request.user
        result.save(update_fields=['validated_by', 'updated_at', 'sync_version'])
        return Response(LabResultSerializer(result).data)


class ImagingOrderListCreateView(generics.ListCreateAPIView):
    serializer_class = ImagingOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['patient', 'modality', 'status']

    def get_queryset(self):
        return ImagingOrder.objects.select_related('patient', 'ordered_by').filter(is_deleted=False)

    def perform_create(self, serializer):
        serializer.save(ordered_by=self.request.user, created_by=self.request.user)


class ImagingOrderDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ImagingOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ImagingOrder.objects.filter(is_deleted=False)
