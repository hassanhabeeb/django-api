from functools import reduce
from rest_framework import generics, status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.blog.schemas import GetAwardListAPISchema, GetBlogListAPISchema, GetEventListAPISchema, GetGalleryListAPISchema, GetPatientStoriesListAPISchema, GetServiceListAPISchema
from apps.blog.serializers import (
    CreateOrUpdateAwardSerializer, 
    CreateOrUpdateBlogSerializer, 
    CreateOrUpdateCommunicationSerializer, 
    CreateOrUpdateEventSerializer, 
    CreateOrUpdateGallerySerializer, 
    CreateOrUpdatePatientStoriesSerializer, 
    CreateOrUpdateServiceSerializer, 
    CreateOrUpdateSubscriptionSerializer, 
    DeleteAwardSerializer, 
    DeleteBlogSerializer, 
    DeleteEventSerializer, 
    DeleteGallerySerializer, 
    DeletePatientStoriesSerializer, 
    DeleteServiceSerializer
)
from breathline.helpers.helper import decode_email, get_object_or_none, get_token_user_or_none
from breathline.helpers.response import ErrorLogInfo, ResponseInfo
from breathline.middleware.JWTAuthentication import BlacklistedJWTAuthentication
from breathline.helpers.custom_messages import _record_not_found,_success
from breathline.helpers.pagination import RestPagination
from apps.blog.models import Blog, Communication, Gallery, Service, PatientStories, Award, Event, Subscription

from drf_yasg import openapi
import os,sys
from django.db.models import Q


class CreateOrUpdateBlogAPIView(generics.GenericAPIView):
    def __init__(self,**kwargs):
        self.response_format = ResponseInfo().response
        super(CreateOrUpdateBlogAPIView,self).__init__(**kwargs)

    serializer_class    = CreateOrUpdateBlogSerializer
    permission_classes  = (IsAuthenticated,)
    authentication_classes    = [BlacklistedJWTAuthentication]

    @swagger_auto_schema(tags=['Blog'])
    def post(self,request):

        try:
            blog_instance  = get_object_or_none(Blog, pk=request.data.get('id',None))

            serializer = self.serializer_class(blog_instance, data=request.data,context={'request':request})
           
            if not serializer.is_valid():
                self.response_format['status_code']           = status.HTTP_400_BAD_REQUEST
                self.response_format['status']                = False
                self.response_format['errors']                = serializer.errors
                return Response(self.response_format,status   = status.HTTP_400_BAD_REQUEST)

            serializer.save()
            self.response_format['status_code']           = status.HTTP_200_OK
            self.response_format['status']                = True
            self.response_format['message']               = _success
            self.response_format['data']                  = {'blog_id': serializer.instance.id}
            return Response(self.response_format,status   = status.HTTP_200_OK)

        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class GetBlogListAPIView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetBlogListAPIView, self).__init__(**kwargs)

    serializer_class = GetBlogListAPISchema
    pagination_class = RestPagination

    search    = openapi.Parameter('search', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="The search by title", required=False)
    slug      = openapi.Parameter('slug', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="The slug field", required=False)

    @swagger_auto_schema(tags=['Blog'], manual_parameters=[search, slug], pagination_class=RestPagination)
    def get(self, request):
        try:
            search    = request.GET.get('search', None)
            slug      = request.GET.get('slug', None)

            filter_queryset = []

            if search not in ['',None]:
                filter_queryset.append(Q(title__icontains=search))

            if slug not in ['',None]:
                filter_queryset.append(Q(slug=slug))

            combined_filters = reduce(lambda x,y:x & y,filter_queryset,Q())
                
            query_set = Blog.objects.filter(combined_filters).order_by('-id').distinct()
        
            page = self.paginate_queryset(query_set)
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
    
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class GetBlogDetailedAPIView(generics.GenericAPIView):
    def __init__(self,**kwargs):
        self.response_format = ResponseInfo().response
        super(GetBlogDetailedAPIView,self).__init__(**kwargs)

    serializer_class    = GetBlogListAPISchema

    id = openapi.Parameter('id',openapi.IN_QUERY,type=openapi.TYPE_STRING,description="The Id",required=True)

    @swagger_auto_schema(tags=['Blog'],manual_parameters=[id])
    def get(self,request):
        try:

            blog_instance = get_object_or_none(Blog,id=request.GET.get('id',None))
            if blog_instance  is None:
                self.response_format['status_code']           = status.HTTP_400_BAD_REQUEST
                self.response_format['status']                = False
                self.response_format['message']               = _record_not_found
                return Response(self.response_format,status   = status.HTTP_400_BAD_REQUEST)

            serializer=self.serializer_class(blog_instance, context={'request':request})
            self.response_format['status_code']           = status.HTTP_200_OK
            self.response_format['status']                = True
            self.response_format['message']               = _success
            self.response_format['data']                  = serializer.data
            return Response(self.response_format,status   = status.HTTP_200_OK)
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class GetBlogDetailedWebAPIView(generics.GenericAPIView):
    def __init__(self,**kwargs):
        self.response_format = ResponseInfo().response
        super(GetBlogDetailedWebAPIView,self).__init__(**kwargs)

    serializer_class    = GetBlogListAPISchema

    id = openapi.Parameter('id',openapi.IN_QUERY,type=openapi.TYPE_STRING,description="The Id",required=True)

    @swagger_auto_schema(tags=['Blog'],manual_parameters=[id])
    def get(self,request):
        try:

            blog_instance = get_object_or_none(Blog,slug=request.GET.get('id',None))
            if blog_instance  is None:
                self.response_format['status_code']           = status.HTTP_400_BAD_REQUEST
                self.response_format['status']                = False
                self.response_format['message']               = _record_not_found
                return Response(self.response_format,status   = status.HTTP_400_BAD_REQUEST)

            serializer=self.serializer_class(blog_instance, context={'request':request})
            self.response_format['status_code']           = status.HTTP_200_OK
            self.response_format['status']                = True
            self.response_format['message']               = _success
            self.response_format['data']                  = serializer.data
            return Response(self.response_format,status   = status.HTTP_200_OK)
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        


class DeleteBlogAPIView(generics.DestroyAPIView): 
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(DeleteBlogAPIView, self).__init__(**kwargs)

    serializer_class = DeleteBlogSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes    = [BlacklistedJWTAuthentication]

    
    @swagger_auto_schema(tags   = ["Blog"], request_body=serializer_class)
    def delete(self, request, *args, **kwargs):
        try: 
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                self.response_format['status_code']             = status.HTTP_400_BAD_REQUEST
                self.response_format["status"]                  = False
                self.response_format["errors"]                  = serializer.errors
                return Response(self.response_format, status    = status.HTTP_400_BAD_REQUEST)

            ids = serializer.validated_data.get('id',[])
            Blog.objects.filter(id__in = ids).delete()

            self.response_format['status_code']             = status.HTTP_200_OK
            self.response_format["message"]                 = _success
            self.response_format["status"]                  = True
            return Response(self.response_format, status    = status.HTTP_200_OK)
            
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


"""Service"""
class CreateOrUpdateServiceURLAPIView(generics.GenericAPIView):
    def __init__(self,**kwargs):
        self.response_format = ResponseInfo().response
        super(CreateOrUpdateServiceURLAPIView,self).__init__(**kwargs)

    serializer_class    = CreateOrUpdateServiceSerializer
    permission_classes  = (IsAuthenticated,)
    authentication_classes    = [BlacklistedJWTAuthentication]

    @swagger_auto_schema(tags=['Service'])
    def post(self,request):

        try:
            service_instance  = get_object_or_none(Service, pk=request.data.get('id',None))

            serializer = self.serializer_class(service_instance, data=request.data,context={'request':request})
           
            if not serializer.is_valid():
                self.response_format['status_code']           = status.HTTP_400_BAD_REQUEST
                self.response_format['status']                = False
                self.response_format['errors']                = serializer.errors
                return Response(self.response_format,status   = status.HTTP_400_BAD_REQUEST)

            serializer.save()
            self.response_format['status_code']           = status.HTTP_200_OK
            self.response_format['status']                = True
            self.response_format['message']               = _success
            self.response_format['data']                  = {'service_instance_id': serializer.instance.id}
            return Response(self.response_format,status   = status.HTTP_200_OK)

        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class GetServiceURLListAPIView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetServiceURLListAPIView, self).__init__(**kwargs)

    serializer_class = GetServiceListAPISchema
    pagination_class = RestPagination

    service_category = openapi.Parameter('service_category', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="The service category", required=False)


    @swagger_auto_schema(tags=['Service'], manual_parameters=[service_category], pagination_class=RestPagination)
    def get(self, request):
        try:
            service_category    = request.GET.get('service_category', None)

            filter_queryset = []

            if service_category not in ['',None]:
                filter_queryset.append(Q(service_category=service_category))

            combined_filters = reduce(lambda x,y:x & y,filter_queryset,Q())
                
            query_set = Service.objects.filter(combined_filters).order_by('-id').distinct()
        
            page = self.paginate_queryset(query_set)
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
    
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class GetServiceURLDetailedAPIView(generics.GenericAPIView):
    def __init__(self,**kwargs):
        self.response_format = ResponseInfo().response
        super(GetServiceURLDetailedAPIView,self).__init__(**kwargs)

    serializer_class    = GetServiceListAPISchema

    id = openapi.Parameter('id',openapi.IN_QUERY,type=openapi.TYPE_STRING,description="The Id",required=True)

    @swagger_auto_schema(tags=['Service'],manual_parameters=[id])
    def get(self,request):
        try:

            service_instance = get_object_or_none(Service,pk=request.GET.get('id',None))
            if service_instance  is None:
                self.response_format['status_code']           = status.HTTP_400_BAD_REQUEST
                self.response_format['status']                = False
                self.response_format['message']               = _record_not_found
                return Response(self.response_format,status   = status.HTTP_400_BAD_REQUEST)

            serializer=self.serializer_class(service_instance, context={'request':request})
            self.response_format['status_code']           = status.HTTP_200_OK
            self.response_format['status']                = True
            self.response_format['message']               = _success
            self.response_format['data']                  = serializer.data
            return Response(self.response_format,status   = status.HTTP_200_OK)
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class DeleteServiceAPIView(generics.DestroyAPIView): 
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(DeleteServiceAPIView, self).__init__(**kwargs)

    serializer_class = DeleteServiceSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes    = [BlacklistedJWTAuthentication]

    
    @swagger_auto_schema(tags   = ["Service"], request_body=serializer_class)
    def delete(self, request, *args, **kwargs):
        try: 
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                self.response_format['status_code']             = status.HTTP_400_BAD_REQUEST
                self.response_format["status"]                  = False
                self.response_format["errors"]                  = serializer.errors
                return Response(self.response_format, status    = status.HTTP_400_BAD_REQUEST)

            ids = serializer.validated_data.get('id',[])
            Service.objects.filter(id__in = ids).delete()

            self.response_format['status_code']             = status.HTTP_200_OK
            self.response_format["message"]                 = _success
            self.response_format["status"]                  = True
            return Response(self.response_format, status    = status.HTTP_200_OK)
            
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""Patient Story"""
class CreateOrUpdatePatientStoriesAPIView(generics.GenericAPIView):

    def __init__(self,**kwargs):
        self.response_format = ResponseInfo().response
        super(CreateOrUpdatePatientStoriesAPIView,self).__init__(**kwargs)

    serializer_class    = CreateOrUpdatePatientStoriesSerializer
    permission_classes  = (IsAuthenticated,)
    authentication_classes    = [BlacklistedJWTAuthentication]

    @swagger_auto_schema(tags=['Patient Stories'])
    def post(self,request):

        try:
            patient_story_instance  = get_object_or_none(PatientStories, pk=request.data.get('id',None))

            serializer = self.serializer_class(patient_story_instance, data=request.data,context={'request':request})
           
            if not serializer.is_valid():
                self.response_format['status_code']           = status.HTTP_400_BAD_REQUEST
                self.response_format['status']                = False
                self.response_format['errors']                = serializer.errors
                return Response(self.response_format,status   = status.HTTP_400_BAD_REQUEST)

            serializer.save()
            self.response_format['status_code']           = status.HTTP_200_OK
            self.response_format['status']                = True
            self.response_format['message']               = _success
            self.response_format['data']                  = {'patient_story_id': serializer.instance.id}
            return Response(self.response_format,status   = status.HTTP_200_OK)

        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class GetPatientStoriesListAPIView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetPatientStoriesListAPIView, self).__init__(**kwargs)

    serializer_class = GetPatientStoriesListAPISchema
    pagination_class = RestPagination

    search    = openapi.Parameter('search', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="The search by name", required=False)

    @swagger_auto_schema(tags=['Patient Stories'], manual_parameters=[search], pagination_class=RestPagination)
    def get(self, request):
        try:
            search    = request.GET.get('search', None)

            filter_queryset = []

            if search not in ['',None]:
                filter_queryset.append(Q(name__icontains=search))

            combined_filters = reduce(lambda x,y:x & y,filter_queryset,Q())
                
            query_set = PatientStories.objects.filter(combined_filters).order_by('-id').distinct()
        
            page = self.paginate_queryset(query_set)
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
    
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetPatientStoriesDetailedAPIView(generics.GenericAPIView):
    def __init__(self,**kwargs):
        self.response_format = ResponseInfo().response
        super(GetPatientStoriesDetailedAPIView,self).__init__(**kwargs)

    serializer_class    = GetPatientStoriesListAPISchema

    id = openapi.Parameter('id',openapi.IN_QUERY,type=openapi.TYPE_STRING,description="The Id",required=True)

    @swagger_auto_schema(tags=['Patient Stories'],manual_parameters=[id])
    def get(self,request):
        try:

            patient_story_instance = get_object_or_none(PatientStories,pk=request.GET.get('id',None))
            if patient_story_instance  is None:
                self.response_format['status_code']           = status.HTTP_400_BAD_REQUEST
                self.response_format['status']                = False
                self.response_format['message']               = _record_not_found
                return Response(self.response_format,status   = status.HTTP_400_BAD_REQUEST)

            serializer=self.serializer_class(patient_story_instance, context={'request':request})
            self.response_format['status_code']           = status.HTTP_200_OK
            self.response_format['status']                = True
            self.response_format['message']               = _success
            self.response_format['data']                  = serializer.data
            return Response(self.response_format,status   = status.HTTP_200_OK)
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class DeletePatientStoriesAPIView(generics.DestroyAPIView): 
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(DeletePatientStoriesAPIView, self).__init__(**kwargs)

    serializer_class = DeletePatientStoriesSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes    = [BlacklistedJWTAuthentication]

    
    @swagger_auto_schema(tags   = ["Patient Stories"], request_body=serializer_class)
    def delete(self, request, *args, **kwargs):
        try: 
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                self.response_format['status_code']             = status.HTTP_400_BAD_REQUEST
                self.response_format["status"]                  = False
                self.response_format["errors"]                  = serializer.errors
                return Response(self.response_format, status    = status.HTTP_400_BAD_REQUEST)

            ids = serializer.validated_data.get('id',[])
            PatientStories.objects.filter(id__in = ids).delete()

            self.response_format['status_code']             = status.HTTP_200_OK
            self.response_format["message"]                 = _success
            self.response_format["status"]                  = True
            return Response(self.response_format, status    = status.HTTP_200_OK)
            
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



"""Gallery"""
class CreateOrUpdateGalleryAPIView(generics.GenericAPIView):

    def __init__(self,**kwargs):
        self.response_format = ResponseInfo().response
        super(CreateOrUpdateGalleryAPIView,self).__init__(**kwargs)

    serializer_class    = CreateOrUpdateGallerySerializer
    permission_classes  = (IsAuthenticated,)
    authentication_classes    = [BlacklistedJWTAuthentication]

    @swagger_auto_schema(tags=['Gallery'])
    def post(self,request):

        try:
            gallery_instance  = get_object_or_none(Gallery, pk=request.data.get('id',None))

            serializer = self.serializer_class(gallery_instance, data=request.data,context={'request':request})
           
            if not serializer.is_valid():
                self.response_format['status_code']           = status.HTTP_400_BAD_REQUEST
                self.response_format['status']                = False
                self.response_format['errors']                = serializer.errors
                return Response(self.response_format,status   = status.HTTP_400_BAD_REQUEST)

            serializer.save()
            self.response_format['status_code']           = status.HTTP_200_OK
            self.response_format['status']                = True
            self.response_format['message']               = _success
            self.response_format['data']                  = {'gallery_instance_id': serializer.instance.id}
            return Response(self.response_format,status   = status.HTTP_200_OK)

        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GetGalleryListAPIView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetGalleryListAPIView, self).__init__(**kwargs)

    serializer_class = GetGalleryListAPISchema
    pagination_class = RestPagination

    @swagger_auto_schema(tags=['Gallery'], manual_parameters=[], pagination_class=RestPagination)
    def get(self, request):
        try:
            filter_queryset = []

            combined_filters = reduce(lambda x,y:x & y,filter_queryset,Q())
                
            query_set = Gallery.objects.filter(combined_filters).order_by('-id').distinct()
        
            page = self.paginate_queryset(query_set)
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
    
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GetGalleryDetailedAPIView(generics.GenericAPIView):
    def __init__(self,**kwargs):
        self.response_format = ResponseInfo().response
        super(GetGalleryDetailedAPIView,self).__init__(**kwargs)

    serializer_class    = GetGalleryListAPISchema

    id = openapi.Parameter('id',openapi.IN_QUERY,type=openapi.TYPE_STRING,description="The Id",required=True)

    @swagger_auto_schema(tags=['Gallery'],manual_parameters=[id])
    def get(self,request):
        try:

            gallery_instance = get_object_or_none(Gallery,pk=request.GET.get('id',None))
            if gallery_instance  is None:
                self.response_format['status_code']           = status.HTTP_400_BAD_REQUEST
                self.response_format['status']                = False
                self.response_format['message']               = _record_not_found
                return Response(self.response_format,status   = status.HTTP_400_BAD_REQUEST)

            serializer=self.serializer_class(gallery_instance, context={'request':request})
            self.response_format['status_code']           = status.HTTP_200_OK
            self.response_format['status']                = True
            self.response_format['message']               = _success
            self.response_format['data']                  = serializer.data
            return Response(self.response_format,status   = status.HTTP_200_OK)
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class DeleteGalleryAPIView(generics.DestroyAPIView): 
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(DeleteGalleryAPIView, self).__init__(**kwargs)

    serializer_class = DeleteGallerySerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes    = [BlacklistedJWTAuthentication]

    
    @swagger_auto_schema(tags   = ["Gallery"], request_body=serializer_class)
    def delete(self, request, *args, **kwargs):
        try: 
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                self.response_format['status_code']             = status.HTTP_400_BAD_REQUEST
                self.response_format["status"]                  = False
                self.response_format["errors"]                  = serializer.errors
                return Response(self.response_format, status    = status.HTTP_400_BAD_REQUEST)

            ids = serializer.validated_data.get('id',[])
            Gallery.objects.filter(id__in = ids).delete()

            self.response_format['status_code']             = status.HTTP_200_OK
            self.response_format["message"]                 = _success
            self.response_format["status"]                  = True
            return Response(self.response_format, status    = status.HTTP_200_OK)
            
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



"""Award"""
class CreateOrUpdateAwardAPIView(generics.GenericAPIView):

    def __init__(self,**kwargs):
        self.response_format = ResponseInfo().response
        super(CreateOrUpdateAwardAPIView,self).__init__(**kwargs)

    serializer_class    = CreateOrUpdateAwardSerializer
    permission_classes  = (IsAuthenticated,)
    authentication_classes    = [BlacklistedJWTAuthentication]

    @swagger_auto_schema(tags=['Award'])
    def post(self,request):

        try:
            award_instance  = get_object_or_none(Award, pk=request.data.get('id',None))

            serializer = self.serializer_class(award_instance, data=request.data,context={'request':request})
           
            if not serializer.is_valid():
                self.response_format['status_code']           = status.HTTP_400_BAD_REQUEST
                self.response_format['status']                = False
                self.response_format['errors']                = serializer.errors
                return Response(self.response_format,status   = status.HTTP_400_BAD_REQUEST)

            serializer.save()
            self.response_format['status_code']           = status.HTTP_200_OK
            self.response_format['status']                = True
            self.response_format['message']               = _success
            self.response_format['data']                  = {'award_instance_id': serializer.instance.id}
            return Response(self.response_format,status   = status.HTTP_200_OK)

        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetAwardListAPIView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetAwardListAPIView, self).__init__(**kwargs)

    serializer_class = GetAwardListAPISchema
    pagination_class = RestPagination

    @swagger_auto_schema(tags=['Award'], manual_parameters=[], pagination_class=RestPagination)
    def get(self, request):
        try:
            filter_queryset = []

            combined_filters = reduce(lambda x,y:x & y,filter_queryset,Q())
                
            query_set = Award.objects.filter(combined_filters).order_by('-id').distinct()
        
            page = self.paginate_queryset(query_set)
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
    
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetAwardDetailedAPIView(generics.GenericAPIView):
    def __init__(self,**kwargs):
        self.response_format = ResponseInfo().response
        super(GetAwardDetailedAPIView,self).__init__(**kwargs)

    serializer_class    = GetAwardListAPISchema

    id = openapi.Parameter('id',openapi.IN_QUERY,type=openapi.TYPE_STRING,description="The Id",required=True)

    @swagger_auto_schema(tags=['Award'],manual_parameters=[id])
    def get(self,request):
        try:

            award_instance = get_object_or_none(Award,pk=request.GET.get('id',None))
            if award_instance  is None:
                self.response_format['status_code']           = status.HTTP_400_BAD_REQUEST
                self.response_format['status']                = False
                self.response_format['message']               = _record_not_found
                return Response(self.response_format,status   = status.HTTP_400_BAD_REQUEST)

            serializer=self.serializer_class(award_instance, context={'request':request})
            self.response_format['status_code']           = status.HTTP_200_OK
            self.response_format['status']                = True
            self.response_format['message']               = _success
            self.response_format['data']                  = serializer.data
            return Response(self.response_format,status   = status.HTTP_200_OK)
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class DeleteAwardAPIView(generics.DestroyAPIView): 
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(DeleteAwardAPIView, self).__init__(**kwargs)

    serializer_class = DeleteAwardSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes    = [BlacklistedJWTAuthentication]

    
    @swagger_auto_schema(tags   = ["Award"], request_body=serializer_class)
    def delete(self, request, *args, **kwargs):
        try: 
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                self.response_format['status_code']             = status.HTTP_400_BAD_REQUEST
                self.response_format["status"]                  = False
                self.response_format["errors"]                  = serializer.errors
                return Response(self.response_format, status    = status.HTTP_400_BAD_REQUEST)

            ids = serializer.validated_data.get('id',[])
            Award.objects.filter(id__in = ids).delete()

            self.response_format['status_code']             = status.HTTP_200_OK
            self.response_format["message"]                 = _success
            self.response_format["status"]                  = True
            return Response(self.response_format, status    = status.HTTP_200_OK)
            
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


"""Event"""
class CreateOrUpdateEventAPIView(generics.GenericAPIView):
    def __init__(self,**kwargs):
        self.response_format = ResponseInfo().response
        super(CreateOrUpdateEventAPIView,self).__init__(**kwargs)

    serializer_class    = CreateOrUpdateEventSerializer
    permission_classes  = (IsAuthenticated,)
    authentication_classes    = [BlacklistedJWTAuthentication]

    @swagger_auto_schema(tags=['Event'])
    def post(self,request):

        try:
            event_instance  = get_object_or_none(Event, pk=request.data.get('id',None))

            serializer = self.serializer_class(event_instance, data=request.data,context={'request':request})
           
            if not serializer.is_valid():
                self.response_format['status_code']           = status.HTTP_400_BAD_REQUEST
                self.response_format['status']                = False
                self.response_format['errors']                = serializer.errors
                return Response(self.response_format,status   = status.HTTP_400_BAD_REQUEST)

            serializer.save()
            self.response_format['status_code']           = status.HTTP_200_OK
            self.response_format['status']                = True
            self.response_format['message']               = _success
            self.response_format['data']                  = {'event_id': serializer.instance.id}
            return Response(self.response_format,status   = status.HTTP_200_OK)

        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetEventListAPIView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetEventListAPIView, self).__init__(**kwargs)

    serializer_class = GetEventListAPISchema
    pagination_class = RestPagination

    @swagger_auto_schema(tags=['Event'], manual_parameters=[], pagination_class=RestPagination)
    def get(self, request):
        try:
            filter_queryset = []

            combined_filters = reduce(lambda x,y:x & y,filter_queryset,Q())
                
            query_set = Event.objects.filter(combined_filters).order_by('-id').distinct()
        
            page = self.paginate_queryset(query_set)
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
    
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GetEventDetailedAPIView(generics.GenericAPIView):
    def __init__(self,**kwargs):
        self.response_format = ResponseInfo().response
        super(GetEventDetailedAPIView,self).__init__(**kwargs)

    serializer_class    = GetEventListAPISchema

    id = openapi.Parameter('id',openapi.IN_QUERY,type=openapi.TYPE_STRING,description="The Id",required=True)

    @swagger_auto_schema(tags=['Event'],manual_parameters=[id])
    def get(self,request):
        try:

            event_instance = get_object_or_none(Event,pk=request.GET.get('id',None))
            if event_instance  is None:
                self.response_format['status_code']           = status.HTTP_400_BAD_REQUEST
                self.response_format['status']                = False
                self.response_format['message']               = _record_not_found
                return Response(self.response_format,status   = status.HTTP_400_BAD_REQUEST)

            serializer=self.serializer_class(event_instance, context={'request':request})
            self.response_format['status_code']           = status.HTTP_200_OK
            self.response_format['status']                = True
            self.response_format['message']               = _success
            self.response_format['data']                  = serializer.data
            return Response(self.response_format,status   = status.HTTP_200_OK)
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class DeleteEventAPIView(generics.DestroyAPIView): 
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(DeleteEventAPIView, self).__init__(**kwargs)

    serializer_class = DeleteEventSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes    = [BlacklistedJWTAuthentication]

    
    @swagger_auto_schema(tags   = ["Event"], request_body=serializer_class)
    def delete(self, request, *args, **kwargs):
        try: 
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                self.response_format['status_code']             = status.HTTP_400_BAD_REQUEST
                self.response_format["status"]                  = False
                self.response_format["errors"]                  = serializer.errors
                return Response(self.response_format, status    = status.HTTP_400_BAD_REQUEST)

            ids = serializer.validated_data.get('id',[])
            Event.objects.filter(id__in = ids).delete()

            self.response_format['status_code']             = status.HTTP_200_OK
            self.response_format["message"]                 = _success
            self.response_format["status"]                  = True
            return Response(self.response_format, status    = status.HTTP_200_OK)
            
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""Subscription"""

class CreateOrUpdateSubscriptionAPIView(generics.GenericAPIView):

    def __init__(self,**kwargs):
        self.response_format = ResponseInfo().response
        super(CreateOrUpdateSubscriptionAPIView,self).__init__(**kwargs)

    serializer_class    = CreateOrUpdateSubscriptionSerializer

    @swagger_auto_schema(tags=['Subscription'])
    def post(self,request):

        try:
            subscription_obj = get_object_or_none(Subscription,email=request.data.get('email',None))
            
            serializer = self.serializer_class(subscription_obj, data=request.data, context={'request':request})

            if not serializer.is_valid():
                self.response_format['status_code']           = status.HTTP_400_BAD_REQUEST
                self.response_format['status']                = False
                self.response_format['errors']                = serializer.errors
                return Response(self.response_format,status   = status.HTTP_400_BAD_REQUEST)

            serializer.save()
            self.response_format['status_code']           = status.HTTP_200_OK
            self.response_format['status']                = True
            self.response_format['message']               = _success
            self.response_format['data']                  = {'subscription_id': serializer.instance.id}
            return Response(self.response_format,status   = status.HTTP_200_OK)

        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

"""Subcribe And UnSubscribe"""
class UnSubScriptionAPIView(generics.GenericAPIView):

    def __init__(self,**kwargs):
        self.response_format = ResponseInfo().response
        super(UnSubScriptionAPIView,self).__init__(**kwargs)

    def post(self,request):

        try:
            email = request.GET.get('email', None)
            encode_email = decode_email(email)
            subscription_obj = get_object_or_none(Subscription,email=encode_email)

            if subscription_obj:
                subscription_obj.is_subscribe = False
                subscription_obj.save()
           
            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = _success
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_200_OK)
            
        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class CreateOrUpdateCommunicationAPIView(generics.GenericAPIView):

    def __init__(self,**kwargs):
        self.response_format = ResponseInfo().response
        super(CreateOrUpdateCommunicationAPIView,self).__init__(**kwargs)

    serializer_class    = CreateOrUpdateCommunicationSerializer

    @swagger_auto_schema(tags=['Communication'])
    def post(self,request):

        try:
            Communication_obj  = get_object_or_none(Communication,pk=request.data.get('id',None))

            serializer = self.serializer_class(Communication_obj,data=request.data,context={'request':request})

            if not serializer.is_valid():
                self.response_format['status_code']           = status.HTTP_400_BAD_REQUEST
                self.response_format['status']                = False
                self.response_format['errors']                = serializer.errors
                return Response(self.response_format,status   = status.HTTP_400_BAD_REQUEST)

            serializer.save()
            self.response_format['status_code']           = status.HTTP_200_OK
            self.response_format['status']                = True
            self.response_format['message']               = _success
            self.response_format['data']                  = {'communication_id': serializer.instance.id}
            return Response(self.response_format,status   = status.HTTP_200_OK)

        except Exception as e:
            error_response = ErrorLogInfo(user_id=request.user.id or None).exception(e)
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)