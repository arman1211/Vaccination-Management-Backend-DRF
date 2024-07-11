from rest_framework import serializers
from rest_framework.response import Response
from .models import VaccineCampaignModel,VaccineDoseBookingModel,VaccineReviewModel
from datetime import timedelta
from patient.serializer import PatientSerializer
from patient.models import PatientModel

class VaccineCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineCampaignModel
        fields = ['id', 'name', 'description', 'start_date', 'end_date','created_by']

class VaccineDoseBookingSerializer(serializers.ModelSerializer):
    vaccine = VaccineCampaignSerializer()
    patient = PatientSerializer()
    class Meta:
        model = VaccineDoseBookingModel
        fields = ['id','vaccine','patient','first_dose_date','second_dose_date']
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
        return dose



class VaccineReviewSerializer(serializers.ModelSerializer):
    # patient = PatientSerializer()
    class Meta:
        model = VaccineReviewModel
        fields = ['id','vaccine','patient','reviews','rating','reviewd_at']
        read_only_fields = ['reviewd_at']
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
