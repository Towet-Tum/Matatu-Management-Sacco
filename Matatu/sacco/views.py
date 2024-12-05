from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User
from sacco.models import Matatu, Driver, Conductor, Route, Revenue, Expense
from sacco.serializers import (
    ManagerSerializer,
    DriverSerializer,
    ConductorSerializer,
    MatatuSerializer,
    RouteSerializer,
    RevenueSerializer,
    ExpenseSerializer,
)
from sacco.permissions import IsManager, IsOwnerOrReadOnly, IsDriverOrConductor


# Managers
class ManagerListView(generics.ListCreateAPIView):
    """
    List all managers or create a new one (Admin only).
    """
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = ManagerSerializer
    permission_classes = [permissions.IsAdminUser]


class ManagerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a manager (Admin only).
    """
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = ManagerSerializer
    permission_classes = [permissions.IsAdminUser]


# Drivers
class DriverListView(generics.ListCreateAPIView):
    """
    List all drivers or create a new one (Manager only).
    """
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]


class DriverDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a driver (Manager only).
    """
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]


# Conductors
class ConductorListView(generics.ListCreateAPIView):
    """
    List all conductors or create a new one (Manager only).
    """
    queryset = Conductor.objects.all()
    serializer_class = ConductorSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]


class ConductorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a conductor (Manager only).
    """
    queryset = Conductor.objects.all()
    serializer_class = ConductorSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]


# Matatus
class MatatuListView(generics.ListCreateAPIView):
    """
    List all Matatus or create a new one (Manager only).
    """
    queryset = Matatu.objects.all()
    serializer_class = MatatuSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MatatuDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a Matatu (Owner only).
    """
    queryset = Matatu.objects.all()
    serializer_class = MatatuSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


# Routes
class RouteListView(generics.ListCreateAPIView):
    """
    List all routes or create a new one (Manager only).
    """
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]


class RouteDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a route (Manager only).
    """
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager]


# Revenue
class RevenueListView(generics.ListCreateAPIView):
    """
    List all revenues or create a new one (Driver or Manager only).
    """
    queryset = Revenue.objects.all()
    serializer_class = RevenueSerializer
    permission_classes = [permissions.IsAuthenticated, IsDriverOrConductor | IsManager]


class RevenueDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a revenue record (Driver, Manager only).
    """
    queryset = Revenue.objects.all()
    serializer_class = RevenueSerializer
    permission_classes = [permissions.IsAuthenticated, IsDriverOrConductor | IsManager]


# Expenses
class ExpenseListView(generics.ListCreateAPIView):
    """
    List all expenses or create a new one (Driver or Manager only).
    """
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated, IsDriverOrConductor | IsManager]


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete an expense record (Driver, Manager only).
    """
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated, IsDriverOrConductor | IsManager]
