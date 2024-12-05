from django.urls import path
from sacco import views

urlpatterns = [
    # Manager URLs
    path('managers/', views.ManagerListView.as_view(), name='manager-list'),
    path('managers/<int:pk>/', views.ManagerDetailView.as_view(), name='manager-detail'),

    # Driver URLs
    path('drivers/', views.DriverListView.as_view(), name='driver-list'),
    path('drivers/<int:pk>/', views.DriverDetailView.as_view(), name='driver-detail'),

    # Conductor URLs
    path('conductors/', views.ConductorListView.as_view(), name='conductor-list'),
    path('conductors/<int:pk>/', views.ConductorDetailView.as_view(), name='conductor-detail'),

    # Matatu URLs
    path('matatus/', views.MatatuListView.as_view(), name='matatu-list'),
    path('matatus/<int:pk>/', views.MatatuDetailView.as_view(), name='matatu-detail'),

    # Route URLs
    path('routes/', views.RouteListView.as_view(), name='route-list'),
    path('routes/<int:pk>/', views.RouteDetailView.as_view(), name='route-detail'),

    # Revenue URLs
    path('revenues/', views.RevenueListView.as_view(), name='revenue-list'),
    path('revenues/<int:pk>/', views.RevenueDetailView.as_view(), name='revenue-detail'),

    # Expense URLs
    path('expenses/', views.ExpenseListView.as_view(), name='expense-list'),
    path('expenses/<int:pk>/', views.ExpenseDetailView.as_view(), name='expense-detail'),
]
