from rest_framework import serializers
from .models import PatientModel,DoctorModel
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id','username', 'password', 'confirm_password', 'email']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            is_active = False
        )
        return user

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = PatientModel
        exclude = ['role']
        
class DoctorSerializer(serializers.ModelSerializer):
    doctor = UserSerializer(many=False)
    class Meta:
        model = DoctorModel
        exclude = ['role']

class PatientRegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = PatientModel
        fields = ['user', 'address', 'phone', 'nid']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.is_active = False
            user = user_serializer.save()
            patient = PatientModel.objects.create(user=user, role='patient', **validated_data)
            return patient
        else:
            raise serializers.ValidationError(user_serializer.errors)
    

class DoctorRegistrationSerializer(serializers.ModelSerializer):
    doctor = UserSerializer()

    class Meta:
        model = PatientModel
        fields = ['doctor', 'address', 'phone', 'nid']

    def create(self, validated_data):
        user_data = validated_data.pop('doctor')
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        doctor = DoctorModel.objects.create(
            doctor=user,
            role='doctor', 
            address=validated_data['address'],
            phone=validated_data['phone'],
            nid=validated_data['nid']
        )
        return doctor