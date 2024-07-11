from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission

# Define user roles as choices
UserRole = [
    ('Patient', 'Patient'),
    ('Doctor', 'Doctor'),
]

class User(AbstractUser):
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    nid = models.CharField(max_length=12, unique=True)
    role = models.CharField(max_length=12, choices=UserRole)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Change related name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  # Change related name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username

class PatientModels(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class DoctorModels(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
