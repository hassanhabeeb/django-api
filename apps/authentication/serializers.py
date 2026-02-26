
from decimal import Decimal
import requests
from rest_framework import serializers

from apps.user.models import Users
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password

import threading
from breathline import settings
from breathline.helpers.helper import get_object_or_none
from breathline.helpers.mail_functions import SendEmails
from django.contrib.auth import authenticate, login


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    class Meta:
        model  = Users
        fields = ['username', 'password']
        
        
        
        

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')   




class UserForgotPasswordChangeSerializer(serializers.Serializer):
    
    new_password        = serializers.CharField(required=True)
    confirm_password    = serializers.CharField(required=True)
    uid                 = serializers.CharField(required=True)
    token               = serializers.CharField(required=True)
    
    def validate(self,attrs):
        return super().validate(attrs)
    





class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)  # Add confirm_password

    class Meta:
        model = Users
        fields = ['username','name', 'email', 'password', 'confirm_password', 'phonenumber','gender'] # 'first_name', 'last_name',
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True},
        }

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        username = data.get('username')
        email = data.get('email')
        # first_name = data.get('first_name')
        # last_name = data.get('last_name')
        name = data.get('name')
        gender = data.get('gender')

        # Check if password and confirm_password match
        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        
        # Password should be at least 7 characters
        if len(password) < 7:
            raise serializers.ValidationError("Password must be at least 7 characters long.")

        # Password should not be entirely numeric
        if password.isdigit():
            raise serializers.ValidationError("Password cannot be entirely numeric.")

        # Password should not be equal to user's personal information
        user_info = [username, email,name,gender] # first_name, last_name,
        if any(info and info.lower() == password.lower() for info in user_info):
            raise serializers.ValidationError("Password should not be the same as your personal information (username, email, first name, or last name).")

        return data

    def create(self, validated_data):
        # Remove confirm_password from validated_data
        validated_data.pop('confirm_password')
        plain_password = validated_data['password']
        
        # Hash the password
        validated_data['password'] = make_password(plain_password)
        user = Users.objects.create(**validated_data)

        # Automatically log in the user
        request = self.context['request']
        authenticated_user = authenticate(username=user.username, password=plain_password)
        if authenticated_user:
            login(request, authenticated_user)

        # Send registration email
        registration_successs_mail(request, user, plain_password)

        return user

def registration_successs_mail(request, instance, password):
    try:
        admin_email = instance.email
        subject = "Welcome To PREP"
        # print("Password to be sent:", password)

        context = {
            'email': admin_email,
            'name': instance.first_name,
            'username': instance.username,
            'user_email': instance.email,
            'password': password,  
            'domain': settings.EMAIL_DOMAIN,
            'protocol': 'https',
        }

        send_email = SendEmails()
        email_thread = threading.Thread(
            target=send_email.sendTemplateEmail, 
            args=(subject, request, context, 'account_created_email.html', settings.EMAIL_HOST_USER, admin_email)
        )
        email_thread.start()

    except Exception as e:
        print(f"Error while sending registration email: {str(e)}")
        pass
