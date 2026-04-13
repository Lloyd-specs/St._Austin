from django.urls import path

from . import views

urlpatterns = [
    path('dashboard/overview/', views.DashboardOverviewView.as_view(), name='dashboard_overview'),
    path('dashboard/epidemiological/', views.EpidemiologicalView.as_view(), name='dashboard_epidemiological'),
    path('dashboard/financial/', views.FinancialView.as_view(), name='dashboard_financial'),
    path('dashboard/pharmacy/', views.PharmacyDashboardView.as_view(), name='dashboard_pharmacy'),
]
