from django.contrib import admin
from .models import PatientModel,DoctorModel

# Register your models here.
admin.site.register(PatientModel)
admin.site.register(DoctorModel)
