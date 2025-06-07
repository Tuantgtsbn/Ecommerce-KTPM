
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomerManager(BaseUserManager):
    def create_user(self, email, username, password=None, customer_type='registered'):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, customer_type=customer_type)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password, customer_type='admin')
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Customer(AbstractBaseUser, PermissionsMixin):
    CUSTOMER_TYPES = [
        ('admin', 'Admin'),
        ('guest', 'Guest'),
        ('registered', 'Registered'),
        ('premium', 'Premium'),
    ]
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPES, default='registered')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
class Address(models.Model):
    customer_id = models.ForeignKey(Customer, related_name="addresses", on_delete=models.CASCADE)
    address_detail = models.TextField()
    street = models.CharField(max_length=255, blank=True, null=True)
    ward = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    province = models.CharField(max_length=255)
    country = models.CharField(max_length=100, )
    is_default = models.BooleanField(default=False)  # Đánh dấu địa chỉ chính

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"
