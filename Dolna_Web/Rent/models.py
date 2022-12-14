from django.db import models

# Create your models here.
class Car(models.Model):
    ID = models.AutoField(primary_key=True)
    DriverID = models.CharField(max_length=255, null=False)
    Model = models.CharField(max_length=255, null=False)
    Color = models.CharField(max_length=100, null=False)
    Type = models.CharField(max_length=255, null=False)
    RegistrationNumber = models.CharField(max_length=255, null=False)
    isAC = models.BooleanField(null=False)
    Condition = models.CharField(max_length=255, null=False)
    Pictures = models.CharField(max_length=255, null=False)

