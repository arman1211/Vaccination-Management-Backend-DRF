from rest_framework import serializers
from .models import PatientModel,Payment
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
    

        

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'email']
    
class UpdatePatientSerializer(serializers.ModelSerializer):
    user = UpdateUserSerializer()

    class Meta:
        model = PatientModel
        fields = ['user', 'address', 'phone', 'nid']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user_serializer = UpdateUserSerializer(instance.user, data=user_data, partial=True)

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
    
class PaymentViewSerializer(serializers.ModelSerializer):
    class Meta:
        model= Payment
        fields= '__all__'
    