from django.contrib import admin
from .models import VaccineCampaignModel,VaccineDoseBookingModel,VaccineReviewModel

# Register your models here.
admin.site.register(VaccineCampaignModel)
admin.site.register(VaccineDoseBookingModel)
admin.site.register(VaccineReviewModel)