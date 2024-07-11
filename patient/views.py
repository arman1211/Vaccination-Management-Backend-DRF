from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import PatientSerializer,PatientRegistrationSerializer,DoctorSerializer,DoctorRegistrationSerializer
from .models import PatientModel,DoctorModel
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User


from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect
# Create your views here.




class PatientView(viewsets.ModelViewSet):
    queryset = PatientModel.objects.all()
    serializer_class = PatientSerializer

class DoctorView(viewsets.ModelViewSet):
    queryset = DoctorModel.objects.all()
    serializer_class = DoctorSerializer


class PatientRegisterView(APIView):
    def post(self, request):
        serializer = PatientRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            patient = serializer.save()
            user = patient.user  # Get the user instance from the patient
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"http://127.0.0.1:8000/patient/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html', {'confirm_link': confirm_link})
            
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response({"message": "Check your mail for confirmation"}, status=200)
        return Response(serializer.errors, status=400)
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DoctorRegisterView(APIView):
    def post(self, request):
        serializer = DoctorRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def activate(request, uid64, token):
    try: 

        uid = urlsafe_base64_decode(uid64).decode() 
        user = User._default_manager.get(pk=uid) 

    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')
    

    