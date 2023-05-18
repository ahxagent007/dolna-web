from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
import hashlib


class Rider(models.Model):
    ID = models.AutoField(primary_key=True)
    FirebaseID = models.CharField(max_length=255, null=False, unique=True)
    Name = models.CharField(max_length=255, null=False)
    Phone = models.CharField(max_length=255, null=False)
    Email = models.CharField(max_length=255, null=False)
    Address = models.CharField(max_length=500, null=False)
    Gender = models.CharField(max_length=50, null=False)
    DateOfBirth = models.DateField(null=False)
    Photo = models.CharField(max_length=255, null=False)

class Driver(models.Model):
    ID = models.AutoField(primary_key=True)
    FirebaseID = models.CharField(max_length=255,null=False)
    Name = models.CharField(max_length=255, null=False)
    Phone = models.CharField(max_length=255, null=False)
    Email = models.CharField(max_length=255, null=False)
    Address = models.CharField(max_length=255, null=False)
    NID = models.CharField(max_length=255, null=False)
    Photo = models.CharField(max_length=4000, null=False)


class CustomUser(BaseUserManager):
    def create_superuser(self, email, phone, password, **other_fields):
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')

        other_fields.setdefault('role', 'ADMIN')
        return self.create_user(email, phone, password, **other_fields)

    def create_user(self, email, phone, password=None, **other_fields):
        if not email:
            raise ValueError(gettext_lazy('Email is required'))
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('role', 'RIDER')
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **other_fields)
        user.password = hashlib.md5(password.encode('utf-8')).hexdigest()

        user.save()
        return user

class UserAccount(AbstractBaseUser):
    user_name = models.CharField(unique=True, max_length=255, null=True, blank=True)
    name = models.CharField(max_length=256, null=False, blank=False)
    email = models.EmailField(unique=True)
    password = models.CharField(null=False, max_length=2000)
    phone = models.CharField(max_length=30, unique=True)
    register_date = models.DateTimeField(default=timezone.now)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)
    is_authenticated = models.BooleanField(default=False)
    objects = CustomUser()

    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        OFFICE = 'STAFF', 'Staff'
        PHOTOGRAPHER = 'DRIVER', 'Driver'
        CUSTOMER = 'RIDER', 'Rider'

    base_role = Role.CUSTOMER

    role = models.CharField(max_length=50, default='RIDER')

    def get_role_list(self):
        return [x.strip() for x in self.role.split(',') if x]

    def set_role_list(self, value):
        self.role = ','.join([x.strip() for x in value if x])

    role_list = property(get_role_list, set_role_list)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser