from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import User



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['id','username','first_name','last_name','email']
        fields = '__all__'