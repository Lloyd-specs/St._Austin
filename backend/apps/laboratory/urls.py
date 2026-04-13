from django.urls import path

from . import views

urlpatterns = [
    path('lab-orders/', views.LabOrderListCreateView.as_view(), name='lab_order_list'),
    path('lab-orders/<uuid:pk>/', views.LabOrderDetailView.as_view(), name='lab_order_detail'),
    path('lab-results/', views.LabResultCreateView.as_view(), name='lab_result_create'),
    path('lab-results/<uuid:pk>/', views.LabResultUpdateView.as_view(), name='lab_result_update'),
    path('lab-results/<uuid:pk>/validate/', views.LabResultValidateView.as_view(), name='lab_result_validate'),
    path('imaging-orders/', views.ImagingOrderListCreateView.as_view(), name='imaging_order_list'),
    path('imaging-orders/<uuid:pk>/', views.ImagingOrderDetailView.as_view(), name='imaging_order_detail'),
]
