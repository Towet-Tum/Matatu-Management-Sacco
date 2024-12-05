from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsManager(BasePermission):
    """
    Custom permission to allow only managers.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Manager').exists()


class IsAdmin(BasePermission):
    """
    Custom permission to allow only admins (superusers).
    """
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsDriver(BasePermission):
    """
    Custom permission to allow only drivers.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Driver').exists()


class IsConductor(BasePermission):
    """
    Custom permission to allow only conductors.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Conductor').exists()


class IsDriverOrConductor(BasePermission):
    """
    Custom permission to allow only drivers or conductors.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=['Driver', 'Conductor']).exists()


class IsRevenueCollector(BasePermission):
    """
    Custom permission to allow only revenue collectors.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Revenue Collector').exists()


class IsRouteManager(BasePermission):
    """
    Custom permission to allow only route managers.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Route Manager').exists()


class IsAuthenticatedAndReadOnly(BasePermission):
    """
    Custom permission to allow only authenticated users to view (read-only access).
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS and request.user.is_authenticated


class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to allow only owners to modify their object.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsManagerOrReadOnly(BasePermission):
    """
    Custom permission to allow managers to edit, others can only read.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.groups.filter(name='Manager').exists()


class IsAdminOrManager(BasePermission):
    """
    Custom permission to allow only admins and managers.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_superuser or 
            request.user.groups.filter(name='Manager').exists()
        )


class IsDriverConductorOrRevenueCollector(BasePermission):
    """
    Custom permission to allow drivers, conductors, or revenue collectors.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=['Driver', 'Conductor', 'Revenue Collector']).exists()


class IsAuthorizedUserForExpenses(BasePermission):
    """
    Custom permission to allow managers or revenue collectors to handle expenses.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=['Manager', 'Revenue Collector']).exists()


class IsManagerOrRouteManager(BasePermission):
    """
    Custom permission to allow only managers or route managers.
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=['Manager', 'Route Manager']).exists()
