from django.contrib import admin
from .models import VaccineCampaignModel,VaccineDoseBookingModel

# Register your models here.
admin.site.register(VaccineCampaignModel)
admin.site.register(VaccineDoseBookingModel)