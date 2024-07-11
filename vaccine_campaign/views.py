from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import VaccineCampaignModel, VaccineDoseBookingModel,VaccineReviewModel
from .serializers import VaccineCampaignSerializer,VaccineDoseBookingSerializer,VaccineReviewSerializer,VaccineDoseBookingCreateSerializer,VaccineReviewPostSerializer
# Create your views here.
class VaccineCampaignViewSet(viewsets.ModelViewSet):
    queryset = VaccineCampaignModel.objects.all()
    serializer_class = VaccineCampaignSerializer

class VaccineCampaignDetailsViewSet(RetrieveAPIView):
    queryset = VaccineCampaignModel.objects.all()
    serializer_class = VaccineCampaignSerializer

class VaccineDoseBookingViewSet(viewsets.ModelViewSet):
    queryset = VaccineDoseBookingModel.objects.all()
    serializer_class = VaccineDoseBookingSerializer

    def perform_create(self, serializer):
        serializer.save()

class VaccineReviewViewSet(viewsets.ModelViewSet):
    queryset = VaccineReviewModel.objects.all()
    serializer_class = VaccineReviewSerializer

    def perform_create(self, serializer):
        serializer.save()

class VaccineDoseBookingCreateView(APIView):
    def post(self, request):
        serializer = VaccineDoseBookingCreateSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save()
            return Response({
                "second_dose_date": booking.second_dose_date
            })
        return Response({"error": "invalid data"})
    
class VaccineReviewPostView(APIView):
    def post(self, request):
        serializer = VaccineReviewPostSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save()
            return Response({
                "success": review
            })
        return Response({"error": "invalid data"})