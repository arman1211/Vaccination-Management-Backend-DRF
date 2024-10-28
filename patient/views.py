from django.shortcuts import render,redirect
from rest_framework.permissions import IsAuthenticated
import logging
import time
import requests
from django.conf import settings
from rest_framework import viewsets,status,generics
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .serializer import PaymentViewSerializer, PatientSerializer,PatientRegistrationSerializer,UpdatePatientSerializer,PasswordUpdateSerializer
from .models import PatientModel, Payment
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from zeep import Client
import json
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect
# Create your views here.




class PatientView(viewsets.ModelViewSet):
    queryset = PatientModel.objects.all()
    serializer_class = PatientSerializer




class PatientRegisterView(APIView):
    def post(self, request):
        serializer = PatientRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            patient = serializer.save()
            user = patient.user  
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"https://vaccination-management-backend-drf.onrender.com/patient/active/{uid}/{token}"
            email_subject = "Confirm Your acount"
            email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
            
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response({"message": "Check your mail for confirmation"}, status=200)
        return Response(serializer.errors, status=400)
    


def activate(request, uid64, token):
    try: 

        uid = urlsafe_base64_decode(uid64).decode() 
        user = User._default_manager.get(pk=uid) 

    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('https://vaccination-management.netlify.app/login')
    else:
        return redirect('https://vaccination-management.netlify.app/register')




class PatientUpdateView(generics.UpdateAPIView):
    queryset = PatientModel.objects.all()
    serializer_class = UpdatePatientSerializer
    lookup_field = 'id'



    
class PasswordUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = PasswordUpdateSerializer

    lookup_field = 'id' 

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(user,serializer.validated_data)
        return Response({"detail": "Password updated successfully"}, status=status.HTTP_200_OK)
    

class InitiatePaymentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        patient = PatientModel.objects.get(user=user)
        
        # Define transaction details
        transaction_id = f"txn_{user.id}_{int(time.time())}"
        amount = 1200.00  # Example amount for premium access
        payment_data = {
            'store_id': settings.SSL_COMMERZ_STORE_ID,
            'store_passwd': settings.SSL_COMMERZ_STORE_PASSWORD,
            'total_amount': amount,
            'currency': 'BDT',
            'tran_id': transaction_id,
            'success_url': settings.SSL_COMMERZ_SUCCESS_URL,
            'fail_url': settings.SSL_COMMERZ_FAIL_URL,
            'cancel_url': settings.SSL_COMMERZ_CANCEL_URL,
            'cus_name': user.username,
            'cus_email': user.email,
            'cus_phone': patient.phone,
            'cus_add1': patient.address,
        }

        # Save payment as pending
        Payment.objects.create(
            patient=patient,
            amount=amount,
            transaction_id=transaction_id,
            status='Pending'
        )

        # Send request to SSL Commerz
        response = requests.post(f"{settings.SSL_COMMERZ_API_URL}/gwprocess/v3/api.php", data=payment_data)
        if response.status_code == 200:
            payment_url = response.json().get("GatewayPageURL")
            return Response({"payment_url": payment_url}, status=200)
        return Response({"error": "Failed to create payment"}, status=500)
    

logger = logging.getLogger(__name__)


class PaymentSuccessView(APIView):
    def post(self, request):
        val_id = request.data.get('val_id')
        transaction_id = request.data.get('tran_id')

        if not val_id or not transaction_id:
            return Response({"error": "val_id or tran_id is missing from the response"}, status=400)

       
        soap_request = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="urn:validationquote">
            <soapenv:Header/>
            <soapenv:Body>
                <tns:checkValidation>
                    <val_id>{val_id}</val_id>
                    <Store_Id>{settings.SSL_COMMERZ_STORE_ID}</Store_Id>
                    <Store_Passwd>{settings.SSL_COMMERZ_STORE_PASSWORD}</Store_Passwd>
                    <v>1</v>
                    <Format>json</Format>
                </tns:checkValidation>
            </soapenv:Body>
        </soapenv:Envelope>
        """

        headers = {
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': 'urn:validationquote#checkValidation',
        }

        try:
            response = requests.post(
                'https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php',
                data=soap_request,
                headers=headers
            )
            response.raise_for_status() 


            response_data = response.content
            json_response = self.extract_json_from_response(response_data)

            if json_response and json_response.get('status') == "VALID":
                payment = Payment.objects.filter(transaction_id=transaction_id).first()
                if payment:
                    payment.status = 'Completed'
                    payment.patient.is_premium = True
                    payment.save()
                    payment.patient.save()
                return redirect(f'https://vaccination-management.netlify.app/pricing/success/{payment.transaction_id}')
            else:
                return Response({"error": "Payment verification failed"}, status=400)

        except requests.exceptions.RequestException as e:
            return Response({"error": f"Error verifying payment: {str(e)}"}, status=500)

    def extract_json_from_response(self, response_data):
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response_data)
        json_data = root.find('.//return').text  
        return json.loads(json_data)


class PaymentFailView(APIView):
    def post(self, request):
        transaction_id = request.data.get('tran_id')
        
       
        payment = Payment.objects.filter(transaction_id=transaction_id).first()
        
        if payment:
            payment.status = 'Failed'
            payment.save()
            return redirect(f'https://vaccination-management.netlify.app/pricing/failed/{payment.transaction_id}')
        return Response({"error": "Transaction ID not found"}, status=404)
    
class PaymentCancelView(APIView):
    def post(self, request):
        transaction_id = request.data.get('tran_id')
        
   
        payment = Payment.objects.filter(transaction_id=transaction_id).first()
        
        if payment:
            payment.status = 'Cancelled'
            payment.save()
            return redirect(f'https://vaccination-management.netlify.app/pricing/canceled/{payment.transaction_id}')
        return Response({"error": "Transaction ID not found"}, status=404)
    
class PaymentDetailView(APIView):
    def get(self, request, transaction_id):
        try:
            payment = Payment.objects.get(transaction_id=transaction_id)
            serializer = PaymentViewSerializer(payment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Payment.DoesNotExist:
            return Response({"error": "Payment record not found"}, status=status.HTTP_404_NOT_FOUND)
class PaymentDetailsByPatientView(APIView):
    def get(self, request, patientId):
        payments = Payment.objects.filter(patient=patientId, status='Completed')
        
        if payments.exists():
            serializer = PaymentViewSerializer(payments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No payment records found for this patient"}, status=status.HTTP_404_NOT_FOUND)