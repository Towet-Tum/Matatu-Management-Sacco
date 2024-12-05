from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser

# Custom User model for role-based authentication
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('driver', 'Driver'),
        ('conductor', 'Conductor'),
        ('owner', 'Matatu Owner'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name="custom_user_set",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="custom_user_set",
        blank=True,
    )


# Route Model
class Route(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Matatu Owner Model
class MatatuOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner_profile')
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


# Matatu Model
class Matatu(models.Model):
    registration_number = models.CharField(max_length=15, unique=True, db_index=True)
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True, related_name='matatus')
    capacity = models.PositiveIntegerField()
    owner = models.ForeignKey(MatatuOwner, on_delete=models.CASCADE, related_name='matatus')
    licence_expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_licence_expired(self):
        return self.licence_expiry_date < now().date()

    def __str__(self):
        return self.registration_number


# Manager Model
class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_profile')
    phone_number = models.CharField(max_length=15)
    assigned_matatus = models.ManyToManyField(Matatu, related_name='managers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


# Driver Model
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    phone_number = models.CharField(max_length=15)
    assigned_matatu = models.OneToOneField(Matatu, on_delete=models.SET_NULL, null=True, blank=True, related_name='driver')
    licence_expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_licence_expired(self):
        return self.licence_expiry_date < now().date()

    def __str__(self):
        return self.user.username


# Conductor Model
class Conductor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='conductor_profile')
    phone_number = models.CharField(max_length=15)
    assigned_driver = models.OneToOneField(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='conductor')
    licence_expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_licence_expired(self):
        return self.licence_expiry_date < now().date()

    def __str__(self):
        return self.user.username


# Revenue Model
class Revenue(models.Model):
    matatu = models.ForeignKey(Matatu, on_delete=models.CASCADE, related_name='revenues')
    amount_collected = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True, db_index=True)
    logged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='revenue_logs')

    class Meta:
        unique_together = ('matatu', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.matatu.registration_number} - {self.amount_collected}"


# Expense Model
class Expense(models.Model):
    matatu = models.ForeignKey(Matatu, on_delete=models.CASCADE, related_name='expenses')
    expense_type = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True, db_index=True)
    logged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='expense_logs')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.matatu.registration_number} - {self.expense_type}"


# Payment Model
class Payment(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments_received")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=50)
    date = models.DateField()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Payment to {self.receiver.username} - {self.amount}"


# Matatu Route Revenue Model
class MatatuRouteRevenue(models.Model):
    matatu = models.ForeignKey(Matatu, on_delete=models.CASCADE, related_name='route_revenues')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='matatu_revenues')
    revenue_collected = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date = models.DateField(default=now, db_index=True)

    class Meta:
        unique_together = ('matatu', 'route', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.matatu.registration_number} - {self.route.name} - {self.date}"


# Route Revenue Model
class RouteRevenue(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='route_revenues')
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    date = models.DateField(default=now, db_index=True)

    class Meta:
        unique_together = ('route', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.route.name} - {self.total_revenue}"
