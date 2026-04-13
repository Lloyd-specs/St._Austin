from django.urls import path

from . import views

urlpatterns = [
    path('sync/push/', views.SyncPushView.as_view(), name='sync_push'),
    path('sync/pull/', views.SyncPullView.as_view(), name='sync_pull'),
    path('sync/conflicts/', views.SyncConflictsView.as_view(), name='sync_conflicts'),
    path('sync/conflicts/<uuid:pk>/resolve/', views.SyncConflictResolveView.as_view(), name='sync_conflict_resolve'),
]
