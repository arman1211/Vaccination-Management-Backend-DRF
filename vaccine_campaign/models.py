from django.db import models
from datetime import timedelta
from django.db import models
from patient.models import DoctorModel ,PatientModel

class VaccineCampaignModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(DoctorModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class VaccineDoseBookingModel(models.Model):
    vaccine = models.ForeignKey(VaccineCampaignModel,on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientModel,on_delete=models.CASCADE)
    first_dose_date = models.DateField()
    second_dose_date = models.DateField(blank=True,null=True)

    def save(self, *args, **kwargs):
        if not self.second_dose_date:
            self.second_dose_date = self.first_dose_date + timedelta(days=30)
        super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.patient.user.username} - {self.vaccine.name}'


Rating = (
    ("⭐","⭐"),
    ("⭐⭐","⭐⭐"),
    ("⭐⭐⭐","⭐⭐⭐"),
    ("⭐⭐⭐⭐","⭐⭐⭐⭐"),
    ("⭐⭐⭐⭐⭐","⭐⭐⭐⭐⭐"),
)

class VaccineReviewModel(models.Model):
    vaccine = models.ForeignKey(VaccineCampaignModel,on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientModel,on_delete=models.CASCADE)
    reviews = models.TextField()
    rating = models.CharField(max_length=20,choices=Rating)
    reviewd_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'reviewd by:- {self.patient.user.username} on {self.vaccine.name}'