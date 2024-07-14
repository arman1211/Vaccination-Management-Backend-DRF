from rest_framework import serializers
from .models import DoctorModel
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
    
class DoctorSerializer(serializers.ModelSerializer):
    doctor = UserSerializer(many=False)
    class Meta:
        model = DoctorModel
        exclude = ['role']

class DoctorRegistrationSerializer(serializers.ModelSerializer):
    doctor = UserSerializer()

    class Meta:
        model = DoctorModel
        fields = ['doctor', 'address', 'phone', 'nid']

    def create(self, validated_data):
        user_data = validated_data.pop('doctor')
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.is_active = False
            user = user_serializer.save()
            doctor = DoctorModel.objects.create(doctor=user, role='doctor', **validated_data)
            return doctor
        else:
            raise serializers.ValidationError(user_serializer.errors)


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'email']

class UpdateDoctorSerializer(serializers.ModelSerializer):
    doctor = UpdateUserSerializer()

    class Meta:
        model = DoctorModel
        fields = ['doctor', 'address', 'phone', 'nid']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('doctor', {})
        user_serializer = UpdateUserSerializer(instance.doctor, data=user_data, partial=True)

        if user_serializer.is_valid(raise_exception=True):
            user_serializer.save()

        instance.address = validated_data.get('address', instance.address)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.nid = validated_data.get('nid', instance.nid)
        instance.save()

        return instance
    

class PasswordUpdateSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only = True,required = True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError('Passwords did not match')
        return data
    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
    
