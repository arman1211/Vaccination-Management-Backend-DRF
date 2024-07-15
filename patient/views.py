from django.shortcuts import render
from rest_framework import viewsets,status,generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import PatientSerializer,PatientRegistrationSerializer,UpdatePatientSerializer,PasswordUpdateSerializer
from .models import PatientModel
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