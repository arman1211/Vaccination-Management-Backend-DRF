from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response



# Create your views here.
class UserLoginApiView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username= username, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({'token' : token.key, 'user_id' : user.id})
            else:
                return Response({'error' : "Invalid Credential"})
        return Response(serializer.errors)
    
class UserLogoutView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')
    