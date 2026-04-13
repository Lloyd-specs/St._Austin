from django.urls import path

from . import views

urlpatterns = [
    path('batches/', views.BatchListCreateView.as_view(), name='batch_list'),
    path('batches/<uuid:pk>/', views.BatchDetailView.as_view(), name='batch_detail'),
    path('stock-movements/', views.StockMovementListCreateView.as_view(), name='stock_movement_list'),
    path('inventory/alerts/', views.InventoryAlertsView.as_view(), name='inventory_alerts'),
]
