from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import User, PatientModels, DoctorModels

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'address', 'phone', 'nid']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class PatientRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = PatientModels
        fields = ['user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            address=user_data['address'],
            phone=user_data['phone'],
            nid=user_data['nid'],
            role='Patient'
        )
        patient = PatientModels.objects.create(user=user)
        return patient

class DoctorRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = DoctorModels
        fields = ['user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            address=user_data['address'],
            phone=user_data['phone'],
            nid=user_data['nid'],
            role='Doctor'
        )
        doctor = DoctorModels.objects.create(user=user)
        return doctor




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['id','username','first_name','last_name','email']
        fields = '__all__'