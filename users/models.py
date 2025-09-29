from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)  # better than CharField

    accountType = models.CharField(max_length=50, choices=[("Freelancer", "Freelancer"), ("Company", "Company")])
    country = models.CharField(max_length=100, blank=True, null=True)
    countryCode = models.CharField(max_length=10, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phoneNumber = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=70, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  
    objects = UserManager()  

    def __str__(self):
        return self.email
    

class Beneficiary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="beneficiaries")
    name = models.CharField(max_length=255)
    bankName = models.CharField(max_length=255)
    accountNumber = models.CharField(max_length=50)
    accountType = models.CharField(max_length=50)
    isDefault = models.BooleanField(default=False)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.accountNumber})"