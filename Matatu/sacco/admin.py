from django.contrib import admin
from .models import User, Matatu, Driver, Conductor, Revenue, Expense, Payment, Manager, MatatuOwner, Route

# Custom User Admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'role')
    list_filter = ('role', 'is_active', 'is_staff')

# Matatu Admin
@admin.register(Matatu)
class MatatuAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'route', 'capacity', 'licence_expiry_date', 'owner', 'is_licence_expired')
    search_fields = ('registration_number', 'route', 'owner__user__username')
    list_filter = ('route', 'owner', 'licence_expiry_date')
    list_editable = ('route',)

# Driver Admin
@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'assigned_matatu', 'licence_expiry_date', 'is_licence_expired')
    search_fields = ('user__username', 'phone_number', 'assigned_matatu__registration_number')
    list_filter = ('licence_expiry_date',)

# Conductor Admin
@admin.register(Conductor)
class ConductorAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'assigned_driver', 'licence_expiry_date', 'is_licence_expired')
    search_fields = ('user__username', 'phone_number', 'assigned_driver__user__username')
    list_filter = ('licence_expiry_date',)

# Matatu Owner Admin
@admin.register(MatatuOwner)
class MatatuOwnerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'created_at')
    search_fields = ('user__username', 'phone_number')
    list_filter = ('created_at',)

# Manager Admin
@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'created_at')
    search_fields = ('user__username', 'phone_number')
    list_filter = ('created_at',)

# Revenue Admin
@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = ('matatu', 'amount_collected', 'date')  # Use 'amount_collected'
    search_fields = ('matatu__registration_number',)
    list_filter = ('date',)

# Expense Admin
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('matatu', 'description', 'amount', 'date')
    search_fields = ('matatu__registration_number', 'description')
    list_filter = ('date',)

# Payment Admin
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('receiver', 'amount', 'date', 'payment_type')
    search_fields = ('receiver__user__username', 'payment_type')
    list_filter = ('date', 'payment_type')

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
