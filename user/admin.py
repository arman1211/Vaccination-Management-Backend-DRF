from django.contrib import admin
from .models import DoctorModels,PatientModels,User
# Register your models here.
admin.site.register(DoctorModels)
admin.site.register(PatientModels)
admin.site.register(User)