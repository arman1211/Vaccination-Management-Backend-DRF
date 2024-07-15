from django.shortcuts import render
from rest_framework import viewsets,status,generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import UpdateDoctorSerializer,DoctorSerializer,DoctorRegistrationSerializer,PasswordUpdateSerializer
from .models import DoctorModel
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User


from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect

# Create your views here.

class DoctorView(viewsets.ModelViewSet):
    queryset = DoctorModel.objects.all()
    serializer_class = DoctorSerializer

class DoctorRegisterView(APIView):
    def post(self, request):
        serializer = DoctorRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            doctor = serializer.save()
            user = doctor.doctor  
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"https://vaccination-management-backend-drf.onrender.com/doctor/active/{uid}/{token}"
            email_subject = "Confirm Your Acount"
            email_body = render_to_string('confirm_emails.html', {'confirm_link': confirm_link})
            
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
        return redirect('https://vaccination-management.netlify.app/register/doctor')

    
class DoctorUpdateView(generics.UpdateAPIView):
    queryset = DoctorModel.objects.all()
    serializer_class = UpdateDoctorSerializer
    lookup_field = 'id'


