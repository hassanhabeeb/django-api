from typing import Any
from django.shortcuts import render
from rest_framework import generics, status
from apps.authentication.schemas import LoginResponseSchema, UserAdminForgotPasswordResponseSchema
from apps.authentication.serializers import  LoginSerializer, LogoutSerializer, UserForgotPasswordChangeSerializer, UserRegistrationSerializer
from apps.user.models import GeneratedAccessToken
import sys, os
from breathline.helpers.helper import get_object_or_none, get_token_user_or_none, update_last_logout
from breathline.helpers.response import ErrorLogInfo, ResponseInfo
from breathline.helpers.custom_messages import _account_tem_suspended, _invalid_credentials
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from django.contrib import auth
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.permissions import IsAuthenticated
from breathline.middleware.JWTAuthentication import BlacklistedJWTAuthentication
from django.utils import timezone
from apps.user.models import Users
from breathline.helpers.custom_messages import _success, _record_not_found
from breathline.helpers.hashing import URLEncryptionDecryption
from breathline.helpers.mail_functions import SendEmails
from django.contrib.auth.tokens import default_token_generator
import threading
from breathline import settings
from django.http import JsonResponse



class LoginApiView(generics.GenericAPIView):
    
    def __init__(self, **kwargs: Any):
        self.response_format = ResponseInfo().response
        super(LoginApiView, self).__init__(**kwargs)
        
    serializer_class = LoginSerializer

    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            # Deserialize the request data using LoginSerializer
            serializer = self.serializer_class(data=request.data)
            
            if not serializer.is_valid():
                # Return errors if the serializer is invalid
                self.response_format['status'] = False
                self.response_format['errors'] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            # Authenticate the user using username and password
            user = auth.authenticate(
                username=serializer.validated_data.get("username", ""),
                password=serializer.validated_data.get("password", ""),
            )
            
            if user:
                # Check if the user's account is inactive
                if not user.is_active:
                    # Provide a clear message indicating the account is inactive
                    self.response_format['status_code'] = status.HTTP_403_FORBIDDEN
                    self.response_format['status'] = False
                    self.response_format['message'] = "Your account is inactive. Please contact support."
                    return Response(self.response_format, status=status.HTTP_403_FORBIDDEN)
                
                else:
                    # Update user login details (mark as logged in, update last login time)
                    user.is_logged_in = True
                    user.last_login = timezone.now()
                    user.save(update_fields=['is_logged_in', 'last_login'])
                    
                    # Serialize user data including first_name, last_name, etc.
                    serializer = LoginResponseSchema(user, context={"request": request})
                    refresh = RefreshToken.for_user(user)
                    token = str(refresh.access_token)
                    
                    # Create response with user data, access token, and refresh token
                    data = {
                        'user': serializer.data,
                        'token': token,
                        'refresh': str(refresh),
                    }
                    
                    # Store the generated access token in the database
                    GeneratedAccessToken.objects.create(user=user, token=token)
                    
                    self.response_format['status_code'] = status.HTTP_200_OK
                    self.response_format['status'] = True
                    self.response_format['data'] = data
                    return Response(self.response_format, status=status.HTTP_200_OK)
            else:
                # Invalid credentials case
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["message"] = "Invalid credentials. Please try again."
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


                
                
class LogoutApiView(generics.GenericAPIView):
    
    def __init__(self, **kwargs: Any):
        self.response_format = ResponseInfo().response
        super(LogoutApiView, self).__init__(**kwargs)
        
    serializer_class          = LogoutSerializer
    permission_classes        = (IsAuthenticated,)
    authentication_classes    = [BlacklistedJWTAuthentication]

    
    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        
        
        try:
            user = get_token_user_or_none(request)
            if user is not None:
                GeneratedAccessToken.objects.filter(user=user).delete()
                update_last_logout(None, user)
            
            self.response_format['status'] = True
            self.response_format['status_code'] = status.HTTP_200_OK
            return Response(self.response_format, status=status.HTTP_200_OK)

        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

"""forgot password"""

class UserAdminForgotPasswordAPIView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(UserAdminForgotPasswordAPIView, self).__init__(**kwargs)
        
    serializer_class = UserAdminForgotPasswordResponseSchema
    @swagger_auto_schema(tags=["Password Management(Admin)"])
    def post(self, request):
        try:
            user_email    = request.data.get('user_email', None)
            user_instance = Users.objects.get(email=user_email)
            
            if user_instance is None:
                self.response_format['status_code'] = status.HTTP_404_NOT_FOUND
                self.response_format['status']      = False
                self.response_format['message']     = _record_not_found
                return Response(self.response_format, status=status.HTTP_404_NOT_FOUND)
            else:
                admin_forgot_password_page_url = f"{os.environ.get('FRONTEND_CMS_URL')}/auth/password/"
                subject = "Password Reset Requested"
                context = {
                    "email"                             : user_email,
                    'domain'                            : settings.EMAIL_DOMAIN,
                    "uid"                               : URLEncryptionDecryption.enc(user_instance.id),
                    "user"                              : user_instance,
                    'token'                             : default_token_generator.make_token(user_instance),
                    'logo_url'                          : settings.API_URL + settings.LOGO_URL,
                    'protocol'                          : 'https',
                    'admin_forgot_password_page_url'    : admin_forgot_password_page_url,
                }
                try:
                    send_email = SendEmails()
                    mail_sending=threading.Thread(target=send_email.sendTemplateEmail, args=(subject, request, context, 'password/admin_forgot_password.html', settings.EMAIL_HOST_USER, user_email))
                    mail_sending.start()
                    
                    self.response_format['status']      = True
                    self.response_format['status_code'] = status.HTTP_200_OK
                    self.response_format['message']     = "Email send successfully and please check the mail"
                    return Response(self.response_format, status=status.HTTP_200_OK)

                except Exception as es:
                    self.response_format['status']      = False
                    self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                    self.response_format['message']     = 'Please enter valid email'
                    return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class AdminPasswordResetConfirmView(generics.GenericAPIView):
    
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(AdminPasswordResetConfirmView, self).__init__(**kwargs)
    
    serializer_class = UserForgotPasswordChangeSerializer
    
    @swagger_auto_schema(tags=["Password Management(Admin)"])
    def post(self, request, *args, **kwargs):
        
        serializer=self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            uid                 = serializer.validated_data.get('uid', None)
            token               = serializer.validated_data.get('token', None)
            confirm_password    = serializer.validated_data.get('confirm_password', None)
            new_password        = serializer.validated_data.get('new_password', None)
        try:
            client_id = URLEncryptionDecryption.dec(uid)
            client = Users.objects.get(id=client_id)
            verify = default_token_generator.check_token(client, token)
            if verify:
                if client:
                    if new_password == confirm_password:
                        client.set_password(new_password)
                        client.save()
                        self.response_format['message']     = 'Password Changed'
                        self.response_format['status_code'] = 100
                    else:
                        self.response_format['message'] = 'Password not Matching'
            else:
                self.response_format['status_code'] = 109
                self.response_format['message']     = 'Please try again'
        except:
            self.response_format['message'] = 'User not found, try again'
            
        return JsonResponse(self.response_format, status=200)
    



class CreateOrUpdateUserApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CreateOrUpdateUserApiView, self).__init__(**kwargs)

    serializer_class = UserRegistrationSerializer
    

    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            
            serializer = self.serializer_class(data=request.data, context={'request': request})

            
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format['status'] = False
                self.response_format['errors'] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

            
            user_instance = get_object_or_none(Users, pk=serializer.validated_data.get('user', None))

            
            serializer = self.serializer_class(user_instance, data=request.data, context={'request': request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format['status'] = False
                self.response_format['errors'] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

            
            serializer.save()

           
            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format['message'] = "User created or updated successfully"
            self.response_format['status'] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)

        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            
