from django.db import models

# Create your models here.

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
    FirebaseID = models.CharField(max_length=255, null=False)
    Name = models.CharField(max_length=255, null=False)
    Phone = models.CharField(max_length=255, null=False)
    Email = models.CharField(max_length=255, null=False)
    Address = models.CharField(max_length=255, null=False)
    NID = models.CharField(max_length=255, null=False)
    Photo = models.CharField(max_length=255, null=False)
