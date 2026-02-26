from functools import reduce
from rest_framework import generics, status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.home.schemas import GetMainBannerImageAPISchema, GetMainBreathVideoAPISchema, GetTestimonialVideoAPISchema
from breathline.helpers.helper import get_object_or_none
from breathline.helpers.response import ErrorLogInfo, ResponseInfo
from breathline.middleware.JWTAuthentication import BlacklistedJWTAuthentication
from breathline.helpers.custom_messages import _record_not_found,_success
from breathline.helpers.pagination import RestPagination
from apps.home.models import MainBannerImage, MainBreathVideo, TestimonialVideo
from apps.home.serializers import CreateOrUpdateMainBannerImageSerializer, CreateOrUpdateMainBreathVideoSerializer, CreateOrUpdateTestimonialVideoSerializer, DeleteMainBannerImageSerializer, DeleteMainBreathVideoSerializer, DeleteTestimonialVideoSerializer
from drf_yasg import openapi
import os,sys
from django.db.models import Q


class CreateOrUpdateMainBannerImageAPIView(generics.GenericAPIView):
    def __init__(self,**kwargs):
        self.response_format = ResponseInfo().response
        super(CreateOrUpdateMainBannerImageAPIView,self).__init__(**kwargs)

    serializer_class    = CreateOrUpdateMainBannerImageSerializer
    permission_classes  = (IsAuthenticated,)
    authentication_classes    = [BlacklistedJWTAuthentication]

    @swagger_auto_schema(tags=['Main Banner Image'])
    def post(self,request):

        try:
            main_banner_instance  = get_object_or_none(MainBannerImage, pk=request.data.get('id',None))

            serializer = self.serializer_class(main_banner_instance, data=request.data,context={'request':request})
           
            if not serializer.is_valid():
                self.response_format['status_code']           = status.HTTP_400_BAD_REQUEST
                self.response_format['status']                = False
                self.response_format['errors']                = serializer.errors
                return Response(self.response_format,status   = status.HTTP_400_BAD_REQUEST)

            serializer.save()
            self.response_format['status_code']           = status.HTTP_200_OK
            self.response_format['status']                = True
            self.response_format['message']               = _success
            self.response_format['data']                  = {'main_banner_instance_id': serializer.instance.id}
            return Response(self.response_format,status   = status.HTTP_200_OK)

        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetMainBannerImageListAPIView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetMainBannerImageListAPIView, self).__init__(**kwargs)

    serializer_class = GetMainBannerImageAPISchema
    pagination_class = RestPagination

    @swagger_auto_schema(tags=['Main Banner Image'], manual_parameters=[], pagination_class=RestPagination)
    def get(self, request):
        try:
            filter_queryset = []

            combined_filters = reduce(lambda x,y:x & y,filter_queryset,Q())
                
            query_set = MainBannerImage.objects.filter(combined_filters).order_by('-id').distinct()
        
            page = self.paginate_queryset(query_set)
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
    
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetMainBannerImageDetailedAPIView(generics.GenericAPIView):
    def __init__(self,**kwargs):
        self.response_format = ResponseInfo().response
        super(GetMainBannerImageDetailedAPIView,self).__init__(**kwargs)

    serializer_class    = GetMainBannerImageAPISchema

    id = openapi.Parameter('id',openapi.IN_QUERY,type=openapi.TYPE_STRING,description="The Id",required=True)

    @swagger_auto_schema(tags=['Main Banner Image'],manual_parameters=[id])
    def get(self,request):
        try:

            main_banner_instance = get_object_or_none(MainBannerImage,pk=request.GET.get('id',None))
            if main_banner_instance  is None:
                self.response_format['status_code']           = status.HTTP_400_BAD_REQUEST
                self.response_format['status']                = False
                self.response_format['message']               = _record_not_found
                return Response(self.response_format,status   = status.HTTP_400_BAD_REQUEST)

            serializer=self.serializer_class(main_banner_instance, context={'request':request})
            self.response_format['status_code']           = status.HTTP_200_OK
            self.response_format['status']                = True
            self.response_format['message']               = _success
            self.response_format['data']                  = serializer.data
            return Response(self.response_format,status   = status.HTTP_200_OK)
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class DeleteMainBannerImageAPIView(generics.DestroyAPIView): 
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(DeleteMainBannerImageAPIView, self).__init__(**kwargs)

    serializer_class = DeleteMainBannerImageSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes    = [BlacklistedJWTAuthentication]

    
    @swagger_auto_schema(tags   = ["Main Banner Image"], request_body=serializer_class)
    def delete(self, request, *args, **kwargs):
        try: 
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                self.response_format['status_code']             = status.HTTP_400_BAD_REQUEST
                self.response_format["status"]                  = False
                self.response_format["errors"]                  = serializer.errors
                return Response(self.response_format, status    = status.HTTP_400_BAD_REQUEST)

            ids = serializer.validated_data.get('id',[])
            MainBannerImage.objects.filter(id__in = ids).delete()

            self.response_format['status_code']             = status.HTTP_200_OK
            self.response_format["message"]                 = _success
            self.response_format["status"]                  = True
            return Response(self.response_format, status    = status.HTTP_200_OK)
            
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateOrUpdateMainBreathVideoAPIView(generics.GenericAPIView):
    def __init__(self,**kwargs):
        self.response_format = ResponseInfo().response
        super(CreateOrUpdateMainBreathVideoAPIView,self).__init__(**kwargs)

    serializer_class    = CreateOrUpdateMainBreathVideoSerializer
    permission_classes  = (IsAuthenticated,)
    authentication_classes    = [BlacklistedJWTAuthentication]

    @swagger_auto_schema(tags=['Main Breath Video'])
    def post(self,request):

        try:
            # breath_video_instance  = get_object_or_none(MainBreathVideo, pk=request.data.get('id',None))
            breath_video_instance  = MainBreathVideo.objects.first()

            serializer = self.serializer_class(breath_video_instance, data=request.data,context={'request':request})
           
            if not serializer.is_valid():
                self.response_format['status_code']           = status.HTTP_400_BAD_REQUEST
                self.response_format['status']                = False
                self.response_format['errors']                = serializer.errors
                return Response(self.response_format,status   = status.HTTP_400_BAD_REQUEST)

            serializer.save()
            self.response_format['status_code']           = status.HTTP_200_OK
            self.response_format['status']                = True
            self.response_format['message']               = _success
            self.response_format['data']                  = {'breath_video_instance_id': serializer.instance.id}
            return Response(self.response_format,status   = status.HTTP_200_OK)

        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class GetMainBreathVideoListAPIView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetMainBreathVideoListAPIView, self).__init__(**kwargs)

    serializer_class = GetMainBreathVideoAPISchema
    pagination_class = RestPagination

    @swagger_auto_schema(tags=['Main Breath Video'], manual_parameters=[], pagination_class=RestPagination)
    def get(self, request):
        try:
            filter_queryset = []

            combined_filters = reduce(lambda x,y:x & y,filter_queryset,Q())
                
            query_set = MainBreathVideo.objects.filter(combined_filters).order_by('-id').distinct()
        
            page = self.paginate_queryset(query_set)
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
    
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class GetMainBreathVideoDetailedAPIView(generics.GenericAPIView):
    def __init__(self,**kwargs):
        self.response_format = ResponseInfo().response
        super(GetMainBreathVideoDetailedAPIView,self).__init__(**kwargs)

    serializer_class    = GetMainBreathVideoAPISchema

    id = openapi.Parameter('id',openapi.IN_QUERY,type=openapi.TYPE_STRING,description="The Id",required=True)

    @swagger_auto_schema(tags=['Main Breath Video'],manual_parameters=[id])
    def get(self,request):
        try:

            # breath_video_instance = get_object_or_none(MainBreathVideo,pk=request.GET.get('id',None))
            breath_video_instance = MainBreathVideo.objects.first()
            if breath_video_instance  is None:
                self.response_format['status_code']           = status.HTTP_400_BAD_REQUEST
                self.response_format['status']                = False
                self.response_format['message']               = _record_not_found
                return Response(self.response_format,status   = status.HTTP_400_BAD_REQUEST)

            serializer=self.serializer_class(breath_video_instance, context={'request':request})
            self.response_format['status_code']           = status.HTTP_200_OK
            self.response_format['status']                = True
            self.response_format['message']               = _success
            self.response_format['data']                  = serializer.data
            return Response(self.response_format,status   = status.HTTP_200_OK)
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class DeleteMainBreathVideoAPIView(generics.DestroyAPIView): 
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(DeleteMainBreathVideoAPIView, self).__init__(**kwargs)

    serializer_class = DeleteMainBreathVideoSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes    = [BlacklistedJWTAuthentication]

    
    @swagger_auto_schema(tags   = ["Main Breath Video"], request_body=serializer_class)
    def delete(self, request, *args, **kwargs):
        try: 
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                self.response_format['status_code']             = status.HTTP_400_BAD_REQUEST
                self.response_format["status"]                  = False
                self.response_format["errors"]                  = serializer.errors
                return Response(self.response_format, status    = status.HTTP_400_BAD_REQUEST)

            ids = serializer.validated_data.get('id',[])
            MainBreathVideo.objects.filter(id__in = ids).delete()

            self.response_format['status_code']             = status.HTTP_200_OK
            self.response_format["message"]                 = _success
            self.response_format["status"]                  = True
            return Response(self.response_format, status    = status.HTTP_200_OK)
            
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

"""TestimonialVideo"""
class CreateOrUpdateTestimonialVideoAPIView(generics.GenericAPIView):
    def __init__(self,**kwargs):
        self.response_format = ResponseInfo().response
        super(CreateOrUpdateTestimonialVideoAPIView,self).__init__(**kwargs)

    serializer_class    = CreateOrUpdateTestimonialVideoSerializer
    permission_classes  = (IsAuthenticated,)
    authentication_classes    = [BlacklistedJWTAuthentication]

    @swagger_auto_schema(tags=['Testimonial Video'])
    def post(self,request):

        try:
            testimonial_instance  = get_object_or_none(TestimonialVideo, pk=request.data.get('id',None))

            serializer = self.serializer_class(testimonial_instance, data=request.data,context={'request':request})
           
            if not serializer.is_valid():
                self.response_format['status_code']           = status.HTTP_400_BAD_REQUEST
                self.response_format['status']                = False
                self.response_format['errors']                = serializer.errors
                return Response(self.response_format,status   = status.HTTP_400_BAD_REQUEST)

            serializer.save()
            self.response_format['status_code']           = status.HTTP_200_OK
            self.response_format['status']                = True
            self.response_format['message']               = _success
            self.response_format['data']                  = {'breath_video_instance_id': serializer.instance.id}
            return Response(self.response_format,status   = status.HTTP_200_OK)

        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetTestimonialVideoListAPIView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetTestimonialVideoListAPIView, self).__init__(**kwargs)

    serializer_class = GetTestimonialVideoAPISchema
    pagination_class = RestPagination

    @swagger_auto_schema(tags=['Testimonial Video'], manual_parameters=[], pagination_class=RestPagination)
    def get(self, request):
        try:
            filter_queryset = []

            combined_filters = reduce(lambda x,y:x & y,filter_queryset,Q())
                
            query_set = TestimonialVideo.objects.filter(combined_filters).order_by('-id').distinct()
        
            page = self.paginate_queryset(query_set)
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
    
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetTestimonialVideoDetailedAPIView(generics.GenericAPIView):
    def __init__(self,**kwargs):
        self.response_format = ResponseInfo().response
        super(GetTestimonialVideoDetailedAPIView,self).__init__(**kwargs)

    serializer_class    = GetTestimonialVideoAPISchema

    id = openapi.Parameter('id',openapi.IN_QUERY,type=openapi.TYPE_STRING,description="The Id",required=True)

    @swagger_auto_schema(tags=['Testimonial Video'],manual_parameters=[id])
    def get(self,request):
        try:

            testimonial_instance = get_object_or_none(TestimonialVideo,pk=request.GET.get('id',None))
            if testimonial_instance  is None:
                self.response_format['status_code']           = status.HTTP_400_BAD_REQUEST
                self.response_format['status']                = False
                self.response_format['message']               = _record_not_found
                return Response(self.response_format,status   = status.HTTP_400_BAD_REQUEST)

            serializer=self.serializer_class(testimonial_instance, context={'request':request})
            self.response_format['status_code']           = status.HTTP_200_OK
            self.response_format['status']                = True
            self.response_format['message']               = _success
            self.response_format['data']                  = serializer.data
            return Response(self.response_format,status   = status.HTTP_200_OK)
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class DeleteTestimonialVideoAPIView(generics.DestroyAPIView): 
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(DeleteTestimonialVideoAPIView, self).__init__(**kwargs)

    serializer_class = DeleteTestimonialVideoSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes    = [BlacklistedJWTAuthentication]

    
    @swagger_auto_schema(tags   = ["Testimonial Video"], request_body=serializer_class)
    def delete(self, request, *args, **kwargs):
        try: 
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                self.response_format['status_code']             = status.HTTP_400_BAD_REQUEST
                self.response_format["status"]                  = False
                self.response_format["errors"]                  = serializer.errors
                return Response(self.response_format, status    = status.HTTP_400_BAD_REQUEST)

            ids = serializer.validated_data.get('id',[])
            TestimonialVideo.objects.filter(id__in = ids).delete()

            self.response_format['status_code']             = status.HTTP_200_OK
            self.response_format["message"]                 = _success
            self.response_format["status"]                  = True
            return Response(self.response_format, status    = status.HTTP_200_OK)
            
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)