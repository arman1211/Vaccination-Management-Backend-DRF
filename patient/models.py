from django.db import models
from django.contrib.auth.models import User


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
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    patient = models.ForeignKey(PatientModel, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


