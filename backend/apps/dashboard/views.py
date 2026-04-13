import datetime

from django.db.models import Count, Sum
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.permissions import IsAdminSystem, IsDirecteur


class DashboardPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role.name in ('admin_systeme', 'directeur')


class DashboardOverviewView(APIView):
    permission_classes = [permissions.IsAuthenticated, DashboardPermission]

    def get(self, request):
        from apps.patients.models import Patient
        from apps.appointments.models import Appointment, QueueEntry
        from apps.billing.models import Invoice

        today = datetime.date.today()

        return Response({
            'patients_total': Patient.objects.filter(is_deleted=False).count(),
            'patients_today': Patient.objects.filter(
                created_at__date=today, is_deleted=False
            ).count(),
            'appointments_today': Appointment.objects.filter(
                scheduled_date=today, is_deleted=False
            ).count(),
            'queue_waiting': QueueEntry.objects.filter(
                status='waiting', is_deleted=False
            ).count(),
            'invoices_pending': Invoice.objects.filter(
                status__in=['pending', 'partially_paid'], is_deleted=False
            ).count(),
            'revenue_today': Invoice.objects.filter(
                status='paid', updated_at__date=today, is_deleted=False
            ).aggregate(total=Sum('total'))['total'] or 0,
        })


class EpidemiologicalView(APIView):
    permission_classes = [permissions.IsAuthenticated, DashboardPermission]

    def get(self, request):
        from apps.medical_records.models import Consultation

        days = int(request.query_params.get('days', 30))
        since = datetime.date.today() - datetime.timedelta(days=days)

        consultations_by_day = (
            Consultation.objects.filter(date__date__gte=since, is_deleted=False)
            .extra(select={'day': "DATE(date)"})
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )

        return Response({
            'period_days': days,
            'consultations_trend': list(consultations_by_day),
            'total_consultations': Consultation.objects.filter(
                date__date__gte=since, is_deleted=False
            ).count(),
        })


class FinancialView(APIView):
    permission_classes = [permissions.IsAuthenticated, DashboardPermission]

    def get(self, request):
        from apps.billing.models import Invoice, Payment

        days = int(request.query_params.get('days', 30))
        since = datetime.date.today() - datetime.timedelta(days=days)

        revenue = Invoice.objects.filter(
            status='paid', updated_at__date__gte=since, is_deleted=False
        ).aggregate(total=Sum('total'))['total'] or 0

        payments_by_method = (
            Payment.objects.filter(
                status='completed', payment_date__date__gte=since, is_deleted=False
            )
            .values('payment_method')
            .annotate(total=Sum('amount'), count=Count('id'))
        )

        outstanding = Invoice.objects.filter(
            status__in=['pending', 'partially_paid'], is_deleted=False
        ).aggregate(total=Sum('amount_due'))['total'] or 0

        return Response({
            'period_days': days,
            'total_revenue': revenue,
            'outstanding_amount': outstanding,
            'payments_by_method': list(payments_by_method),
        })


class PharmacyDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated, DashboardPermission]

    def get(self, request):
        from apps.inventory.models import Batch
        from apps.pharmacy.models import Medication

        today = datetime.date.today()
        days_30 = today + datetime.timedelta(days=30)

        return Response({
            'total_medications': Medication.objects.filter(is_active=True, is_deleted=False).count(),
            'expiring_soon': Batch.objects.filter(
                expiry_date__lte=days_30, expiry_date__gt=today,
                quantity_remaining__gt=0, is_deleted=False,
            ).count(),
            'expired': Batch.objects.filter(
                expiry_date__lte=today, quantity_remaining__gt=0, is_deleted=False,
            ).count(),
            'total_stock_value': Batch.objects.filter(
                quantity_remaining__gt=0, is_deleted=False,
            ).aggregate(
                total=Sum('quantity_remaining') * Sum('unit_cost')
            )['total'] or 0,
        })
