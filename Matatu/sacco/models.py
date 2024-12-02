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
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="custom_user_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )
#Route Model
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
        return f"{self.user.username} - Owner"

# Matatu Model
class Matatu(models.Model):
    registration_number = models.CharField(max_length=15, unique=True, db_index=True)
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True, related_name='matatus')
    capacity = models.PositiveIntegerField()
    owner = models.ForeignKey(MatatuOwner, on_delete=models.CASCADE, related_name='matatus')
    licence_expiry_date = models.DateField()  # Added expiry date for Matatu license
    created_at = models.DateTimeField(auto_now_add=True)

    def is_licence_expired(self):
        return self.licence_expiry_date < now().date()

    def __str__(self):
        return f"{self.registration_number} - {self.route.name if self.route else 'No Route'}"

# Manager Model
class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_profile')
    phone_number = models.CharField(max_length=15)
    assigned_matatus = models.ManyToManyField(Matatu, related_name='managers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Manager"

# Driver Model
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    phone_number = models.CharField(max_length=15)
    assigned_matatu = models.OneToOneField(Matatu, on_delete=models.SET_NULL, null=True, blank=True, related_name='driver')
    licence_expiry_date = models.DateField()  # Added expiry date for Driver's license
    created_at = models.DateTimeField(auto_now_add=True)

    def is_licence_expired(self):
        return self.licence_expiry_date < now().date()

    def __str__(self):
        return f"{self.user.username} - Driver"

# Conductor Model
class Conductor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='conductor_profile')
    phone_number = models.CharField(max_length=15)
    assigned_driver = models.OneToOneField(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='conductor')
    licence_expiry_date = models.DateField()  # Added expiry date for Conductor's license
    created_at = models.DateTimeField(auto_now_add=True)

    def is_licence_expired(self):
        return self.licence_expiry_date < now().date()

    def __str__(self):
        return f"{self.user.username} - Conductor"


# Revenue Model
class Revenue(models.Model):
    matatu = models.ForeignKey(Matatu, on_delete=models.CASCADE, related_name='revenues')
    amount_collected = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True, db_index=True)
    logged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='revenue_logs')

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

    def __str__(self):
        return f"{self.matatu.registration_number} - {self.expense_type} - {self.amount}"

# Payment Model
class Payment(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments_received")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=50)
    date = models.DateField()

    def __str__(self):
        return f"Payment to {self.receiver.username} - {self.amount}"
