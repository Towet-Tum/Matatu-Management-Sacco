from rest_framework import serializers
from django.utils.timezone import now

from .models import (Matatu, 
                     Route, 
                     Driver, 
                     Conductor, 
                     Revenue, Payment, 
                     MatatuOwner, 
                     Manager, 
                     RouteRevenue, 
                     MatatuRouteRevenue,
                     Expense)

class MatatuSerializer(serializers.ModelSerializer):
    
    def validate_registration_number(self, value):
        """Ensure the registration number is alphanumeric."""
        if not value.isalnum():
            raise serializers.ValidationError("Registration number must be alphanumeric.")
        return value
    
    def validate_licence_expiry_date(self, value):
        """Ensure the license expiry date is in the future."""
        if value <= now().date():
            raise serializers.ValidationError("License expiry date must be in the future.")
        return value

    class Meta:
        model = Matatu
        fields = ['id', 'registration_number', 'route', 'capacity', 'licence_expiry_date', 'owner']




class RouteSerializer(serializers.ModelSerializer):

    def validate_route_number(self, value):
        """Ensure the route number is unique."""
        if Route.objects.filter(route_number=value).exists():
            raise serializers.ValidationError("This route number already exists.")
        return value

    def validate(self, data):
        """Ensure start and end locations are not the same."""
        if data['start_location'] == data['end_location']:
            raise serializers.ValidationError("Start and end locations cannot be the same.")
        return data

    class Meta:
        model = Route
        fields = ['id', 'route_number', 'start_location', 'end_location', 'distance_km']




class DriverSerializer(serializers.ModelSerializer):

    def validate_licence_expiry_date(self, value):
        """Ensure the driver's license expiry date is in the future."""
        if value <= now().date():
            raise serializers.ValidationError("Driver's license must not be expired.")
        return value
    
    def validate(self, data):
        """Ensure driver is assigned to a valid matatu."""
        if data.get('assigned_matatu') and not data['assigned_matatu'].is_active:
            raise serializers.ValidationError("Assigned matatu is not active.")
        return data

    class Meta:
        model = Driver
        fields = ['id', 'name', 'licence_number', 'licence_expiry_date', 'assigned_matatu']
        
class RevenueSerializer(serializers.ModelSerializer):

    def validate_amount_collected(self, value):
        """Ensure the amount collected is greater than zero."""
        if value <= 0:
            raise serializers.ValidationError("Amount collected must be greater than 0.")
        return value

    def validate_amount(self, value):
        """Ensure the amount is positive."""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate(self, data):
        """Ensure the matatu and route are valid and active."""
        matatu = data.get('matatu')
        route = data.get('route')
        if matatu and not matatu.is_active:
            raise serializers.ValidationError("The matatu is not active.")
        if route and not route.is_active:
            raise serializers.ValidationError("The route is not active.")
        return data

    class Meta:
        model = MatatuRouteRevenue
        fields = ['id', 'matatu', 'route', 'amount', 'date']
    
    def validate(self, data):
        """Ensure the matatu is valid and active."""
        matatu = data.get('matatu')
        if matatu and not matatu.is_active:
            raise serializers.ValidationError("The matatu is not active.")
        return data

    class Meta:
        model = Revenue
        fields = ['id', 'matatu', 'amount_collected', 'date', 'logged_by']
        
        
class RouteRevenueSerializer(serializers.ModelSerializer):

    def validate_amount(self, value):
        """Ensure the amount is positive."""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
    
    def validate(self, data):
        """Ensure the route is valid."""
        route = data.get('route')
        if route and not route.is_active:
            raise serializers.ValidationError("The route is not active.")
        return data

    class Meta:
        model = RouteRevenue
        fields = ['id', 'route', 'amount', 'date']


class MatatuRouteRevenueSerializer(serializers.ModelSerializer):

    def validate_amount(self, value):
        """Ensure the amount is positive."""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate(self, data):
        """Ensure the matatu and route are valid and active."""
        matatu = data.get('matatu')
        route = data.get('route')
        if matatu and not matatu.is_active:
            raise serializers.ValidationError("The matatu is not active.")
        if route and not route.is_active:
            raise serializers.ValidationError("The route is not active.")
        return data

    class Meta:
        model = MatatuRouteRevenue
        fields = ['id', 'matatu', 'route', 'amount', 'date']

class MatatuOwnerSerializer(serializers.ModelSerializer):
    
    def validate_phone_number(self, value):
        """Ensure the phone number is valid."""
        if not value.isdigit() or len(value) not in [10, 12]:
            raise serializers.ValidationError("Phone number must be numeric and either 10 or 12 digits long.")
        if MatatuOwner.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already registered.")
        return value

    class Meta:
        model = MatatuOwner
        fields = ['id', 'name', 'email', 'phone_number']
        
        
class ConductorSerializer(serializers.ModelSerializer):

    def validate_phone_number(self, value):
        """Ensure the phone number is valid."""
        if not value.isdigit() or len(value) not in [10, 12]:
            raise serializers.ValidationError("Phone number must be numeric and either 10 or 12 digits long.")
        return value

    def validate(self, data):
        """Ensure the assigned matatu is active."""
        matatu = data.get('assigned_matatu')
        if matatu and not matatu.is_active:
            raise serializers.ValidationError("Assigned matatu is not active.")
        return data

    class Meta:
        model = Conductor
        fields = ['id', 'name', 'phone_number', 'assigned_matatu']
        
        
class ManagerSerializer(serializers.ModelSerializer):
    
    def validate_phone_number(self, value):
        """Ensure the phone number is valid."""
        if not value.isdigit() or len(value) not in [10, 12]:
            raise serializers.ValidationError("Phone number must be numeric and either 10 or 12 digits long.")
        return value
    
    def validate(self, data):
        """Ensure the manager is associated with at least one valid matatu."""
        matatus = data.get('assigned_matatus')  # Updated to match the field in the model
        if matatus and not all(matatu.is_active for matatu in matatus):
            raise serializers.ValidationError("All managed matatus must be active.")
        return data

    class Meta:
        model = Manager
        fields = ['id', 'user', 'phone_number', 'assigned_matatus']  # Removed 'name' and added 'user'
        depth = 1  # To include nested 'user' data if needed

        

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'