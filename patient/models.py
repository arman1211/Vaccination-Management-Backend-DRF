from django.db import models
from django.contrib.auth.models import AbstractUser,User

# Create your models here.
UserRole = (
    ('patient','patient'),
    ('doctor','doctor')
)

class PatientModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    nid = models.CharField(max_length=12,unique=True)
    role = models.CharField(max_length=12,choices=UserRole)

    def __str__(self):
        return self.user.username

class DoctorModel(models.Model):
    doctor = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    nid = models.CharField(max_length=12,unique=True)
    role = models.CharField(max_length=12,choices=UserRole)

    def __str__(self):
        return self.doctor.username

