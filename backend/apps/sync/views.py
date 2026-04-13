from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ConflictRecord, SyncLog
from .serializers import ConflictRecordSerializer, SyncLogSerializer


class SyncPushView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        changes = request.data.get('changes', [])
        device_id = request.data.get('device_id', '')
        results = []

        for change in changes:
            log = SyncLog.objects.create(
                device_id=device_id,
                user=request.user,
                sync_type='push',
                entity_type=change.get('entity_type', ''),
                entity_id=change.get('entity_id', ''),
                action=change.get('action', 'update'),
                payload=change.get('payload', {}),
                status='applied',
                created_by=request.user,
            )
            results.append(SyncLogSerializer(log).data)

        return Response({'applied': len(results), 'results': results})


class SyncPullView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        since = request.query_params.get('since')
        # Placeholder: return empty changes for now
        return Response({
            'changes': [],
            'server_timestamp': timezone.now().isoformat(),
        })


class SyncConflictsView(generics.ListAPIView):
    serializer_class = SyncLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SyncLog.objects.filter(
            user=self.request.user, status='conflict', is_deleted=False,
        ).prefetch_related('conflicts')


class SyncConflictResolveView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            conflict = ConflictRecord.objects.get(pk=pk, is_deleted=False)
        except ConflictRecord.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        resolved_value = request.data.get('resolved_value', '')
        conflict.resolved_value = resolved_value
        conflict.resolved_at = timezone.now()
        conflict.save()

        # Check if all conflicts for the sync log are resolved
        sync_log = conflict.sync_log
        unresolved = sync_log.conflicts.filter(resolved_at__isnull=True).count()
        if unresolved == 0:
            sync_log.status = 'applied'
            sync_log.conflict_resolved_by = 'manual'
            sync_log.save(update_fields=['status', 'conflict_resolved_by', 'updated_at', 'sync_version'])

        return Response(ConflictRecordSerializer(conflict).data)
