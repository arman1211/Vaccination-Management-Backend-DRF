from django.contrib import admin
from .models import PatientModel,Payment

# Register your models here.
admin.site.register(PatientModel)
admin.site.register(Payment)

