from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.pharmacy.models import Medication

from .models import VerificationLog
from .serializers import VerificationLogSerializer


class VerifyBarcodeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        barcode = request.data.get('barcode', '')
        if not barcode:
            return Response(
                {'detail': 'Code-barres requis.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Look up medication by barcode
        medication = Medication.objects.filter(barcode=barcode, is_deleted=False).first()

        if medication:
            result = 'authentic'
            confidence = 1.0
        else:
            result = 'unknown'
            confidence = 0.0

        log = VerificationLog.objects.create(
            medication=medication,
            barcode_data=barcode,
            verification_method='barcode',
            result=result,
            confidence_score=confidence,
            verified_by=request.user,
            created_by=request.user,
        )
        return Response(VerificationLogSerializer(log).data, status=status.HTTP_201_CREATED)


class VerifyImageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        image = request.FILES.get('image')
        if not image:
            return Response(
                {'detail': 'Image requise.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # AI verification stub - returns unknown until model is trained
        log = VerificationLog.objects.create(
            barcode_data='image_verification',
            verification_method='ai_image',
            result='unknown',
            confidence_score=0.0,
            image=image,
            verified_by=request.user,
            created_by=request.user,
            details={'message': 'AI model not yet deployed. Manual verification required.'},
        )
        return Response(VerificationLogSerializer(log).data, status=status.HTTP_201_CREATED)


class VerificationLogListView(generics.ListAPIView):
    serializer_class = VerificationLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['result', 'verification_method']

    def get_queryset(self):
        return VerificationLog.objects.select_related('medication').filter(is_deleted=False)


class VerificationLogDetailView(generics.RetrieveAPIView):
    serializer_class = VerificationLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = VerificationLog.objects.filter(is_deleted=False)
