from rest_framework import serializers
from rest_framework.response import Response
from .models import VaccineCampaignModel,VaccineDoseBookingModel,VaccineReviewModel
from datetime import timedelta
from patient.serializer import PatientSerializer
from patient.models import PatientModel

from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect

class VaccineCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineCampaignModel
        fields = ['id', 'name', 'description', 'start_date', 'end_date','created_by','image']

class VaccineDoseBookingSerializer(serializers.ModelSerializer):
    vaccine = VaccineCampaignSerializer()
    patient = PatientSerializer()
    class Meta:
        model = VaccineDoseBookingModel
        fields = ['id','vaccine','patient','first_dose_date','second_dose_date','is_completed']
        read_only_fields = ['second_dose_date']
    def validate_first_dose_date(self, value):
        vaccine = self.initial_data.get('vaccine')
        vaccine_campaign = VaccineCampaignModel.objects.get(id=vaccine)
        if value > vaccine_campaign.end_date:
            return serializers.ValidationError("First dose date cannot be later than the vaccine campaign end date.")
        return value
    def create(self, validated_data):
        first_dose_date = validated_data.get('first_dose_date')
        validated_data['second_dose_date'] = first_dose_date + timedelta(days=30)
        return super().create(validated_data)
    


    
class VaccineDoseBookingCreateSerializer(serializers.ModelSerializer):
    patient_id = serializers.IntegerField(write_only=True)
    vaccine_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = VaccineDoseBookingModel
        fields = ['patient_id', 'vaccine_id', 'first_dose_date']

    def validate_first_dose_date(self, value):
        vaccine_id = self.initial_data.get('vaccine_id')
        vaccine_campaign = VaccineCampaignModel.objects.get(id=vaccine_id)
        if value > vaccine_campaign.end_date:
            raise serializers.ValidationError("First dose date cannot be later than the vaccine campaign end date.")
        return value

    def create(self, validated_data):
        patient_id = validated_data.pop('patient_id')
        vaccine_id = validated_data.pop('vaccine_id')

        patient = PatientModel.objects.get(id=patient_id)
        vaccine = VaccineCampaignModel.objects.get(id=vaccine_id)

        first_dose_date = validated_data.get('first_dose_date')
        second_dose_date = first_dose_date + timedelta(days=30)

        dose = VaccineDoseBookingModel.objects.create(
            patient=patient,
            vaccine=vaccine,
            first_dose_date=first_dose_date,
            second_dose_date=second_dose_date
        )
        self.send_email_notification(patient,vaccine,first_dose_date,second_dose_date)
        return dose
    def send_email_notification(self, patient, vaccine, first_dose_date, second_dose_date):
        context = {
            'patient':patient,
            'vaccine': vaccine,
            'first_dose_date': first_dose_date,
            'second_dose_date': second_dose_date
        }

        email_subject = "Confirm Your Appointment"
        email_body = render_to_string('appointment_email.html', {'context':context})
        
        email = EmailMultiAlternatives(email_subject, '', to=[patient.user.email])
        email.attach_alternative(email_body, "text/html")
        email.send()
    
class VaccineDoseBookingCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineDoseBookingModel
        fields = ['is_completed']

    def update(self, instance, validated_data):
        instance.is_completed = validated_data.get('is_completed', instance.is_completed)
        instance.save()
        return instance



class VaccineReviewSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    class Meta:
        model = VaccineReviewModel
        fields = ['id','vaccine','patient','reviews','rating','reviewd_at','patient_name']
        read_only_fields = ['reviewd_at','patient_name']
    def get_patient_name(self, obj):
        return obj.patient.user.username
    def validate(self, data):
        vaccine = data['vaccine']
        patient = data['patient']

        if not VaccineDoseBookingModel.objects.filter(vaccine = vaccine , patient=patient).exists():
            raise serializers.ValidationError({"error": "You cannot leave a review for a campaign you haven't booked."})
        return data
    
class VaccineReviewPostSerializer(serializers.ModelSerializer):
    patient_id = serializers.IntegerField(write_only = True)
    class Meta:
        model = VaccineReviewModel
        fields = ['id','vaccine','patient_id','reviews','rating','reviewd_at']
        read_only_fields = ['reviewd_at']
    def create(self, validated_data):
        patient_id = validated_data.pop('patient_id')
        vaccine = validated_data.pop['vaccine']
        patient = PatientModel.objects.get(id = patient_id)

        if not VaccineDoseBookingModel.objects.filter(vaccine = vaccine , patient=patient).exists():
            raise serializers.ValidationError({"error": "You cannot leave a review for a campaign you haven't booked."})
        review = VaccineReviewModel.objects.create(vaccine=vaccine, patient=patient, **validated_data)
        return review
