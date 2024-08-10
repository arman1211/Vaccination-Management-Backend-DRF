import os
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import get_object_or_404
from .models import VaccineDoseBookingModel
from rest_framework import status
from rest_framework.generics import RetrieveAPIView,UpdateAPIView,DestroyAPIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import VaccineCampaignModel, VaccineDoseBookingModel,VaccineReviewModel
from .serializers import VaccineDoseBookingCompletionSerializer, VaccineCampaignSerializer,VaccineDoseBookingSerializer,VaccineReviewSerializer,VaccineDoseBookingCreateSerializer,VaccineReviewPostSerializer
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
    queryset = VaccineReviewModel.objects.all().order_by('-reviewd_at')[:4]
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

class CompleteDoseView(UpdateAPIView):
    queryset = VaccineDoseBookingModel.objects.all()
    serializer_class = VaccineDoseBookingCompletionSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_completed = True
        instance.save()
        return Response({"detail": "Dose marked as completed"}, status=status.HTTP_200_OK)
    
class UpdateVaccineCampaignView(UpdateAPIView):
    queryset = VaccineCampaignModel.objects.all()
    serializer_class = VaccineCampaignSerializer
    lookup_field = 'id'

    def perform_update(self, serializer):
        instance = serializer.save(Partial=True)
        instance.save()

class DeleteVaccineCampaignView(DestroyAPIView):
    queryset = VaccineCampaignModel.objects.all()
    lookup_field = 'id'

class DeleteVaccineDoseBooking(DestroyAPIView):
    queryset = VaccineDoseBookingModel.objects.all()
    lookup_field = 'id'


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def generate_pdf_report(request, id):
    booking = get_object_or_404(VaccineDoseBookingModel, id=id)
    if booking.is_completed == True:
        vaccine_status = 'Completed'
    else:
        vaccine_status = 'Pending'
    context = {
        'patient': booking.patient.user.username,
        'vaccine': booking.vaccine.name,
        'first_dose_date': booking.first_dose_date,
        'second_dose_date': booking.second_dose_date,
        'is_completed': vaccine_status
    }
    pdf = render_to_pdf('appointment_report.html', context)
    return HttpResponse(pdf, content_type='application/pdf')