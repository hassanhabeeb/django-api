


import random
from uuid import uuid4
from django.contrib.auth.models import Permission
from rest_framework import serializers
from django_acl.models import Group, Role
from django.contrib.auth.models import Permission
from apps.user.models import Users
"""_summary_
PERMISSION LISTING RESPONSE SCHEMAS 
"""

class RetrieveUsersSchema(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['pk','username','email','is_active','is_admin','is_staff']


class GetUserListDropdownApiResposceSchemas(serializers.ModelSerializer):
    value = serializers.IntegerField(source='pk')
    label = serializers.CharField(source='username')
    class Meta:
        model = Users
        fields = ['value','label','is_logged_in']


    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas


class GetUserGroupsSerializer(serializers.ModelSerializer):
    
    value    =  serializers.IntegerField(source='pk')
    label    =  serializers.CharField(source='name')
    class Meta:
        model  = Permission
        fields = ['value','label']


class RetrieveUserInfoApiSchema(serializers.ModelSerializer):
    user_groups             = serializers.SerializerMethodField('get_user_groups')
    
    class Meta:
        model = Users
        fields = ['username','email','is_password_reset_required','is_active','is_admin','is_staff','user_groups']
        
        
    def get_user_groups(self,obj):
        return GetUserGroupsSerializer(obj.user_groups.all(),many=True).data
      
    
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas
    
class GetPermissionsSerializer(serializers.ModelSerializer):
    

    label    =  serializers.CharField(source='name')
    class Meta:
        model  = Permission
        fields = ['id','label']

class PermissionSerializer(serializers.ModelSerializer):
    childNodes    = serializers.SerializerMethodField('get_children')
    # label    =  serializers.SerializerMethodField('get_label')
    id            = serializers.SerializerMethodField('get_label')
    label         = serializers.CharField(source='sub_label')
    class Meta:
        model  = Permission
        fields = ['label','id', 'childNodes']
        
        
    def get_children(self, obj):
        permissions = Permission.objects.filter(label=obj.label).filter(sub_label=obj.sub_label)
        permission_serializer = GetPermissionsSerializer(permissions, many=True)
        return permission_serializer.data
    
    
    def get_label(self, obj):
        return "{}".format(uuid4())



class PermissionsResponceSchema(serializers.ModelSerializer):
    
    
    childNodes = serializers.SerializerMethodField('get_children')
    id    =  serializers.CharField(source='label')

    class Meta:
        model  = Permission
        fields = ['id','label', 'childNodes']
        
    
    def get_children(self, obj):
        permissions = Permission.objects.filter(label=obj.label).order_by('sub_label').distinct('sub_label')
        permission_serializer = PermissionSerializer(permissions, many=True)
        return permission_serializer.data
    
    def to_representation(self, instance):
        data = super().to_representation(instance)

        for field in data:
            if data[field] is None:
                data[field] = ""

        return data
        
    


# class GetPermissionResponseSchemas(serializers.ModelSerializer):
#     children = serializers.SerializerMethodField('get_children')
#     value    =  serializers.SerializerMethodField('get_label')
#     label    =  serializers.CharField(source='sub_label')
#     class Meta:
#         model  = Permission
#         fields = ['label','value', 'children']
        
        
#     def get_children(self, obj):
#         permissions = Permission.objects.filter(label=obj.label).filter(sub_label=obj.sub_label)
#         permission_serializer = GetPermissionsResponseSchemas(permissions, many=True)
#         if permission_serializer:
#             return permission_serializer.data
#         return []
    
    
#     def get_label(self, obj):
#         return "{}".format(uuid4())
        

# class GetPermissionSchemas(serializers.ModelSerializer):
#     children = serializers.SerializerMethodField('get_children')
#     value = serializers.CharField(source='label')

#     class Meta:
#         model = Permission
#         fields = ['label', 'value', 'children']

#     def get_children(self, obj):
#         permissions = Permission.objects.filter(label=obj.label).order_by('sub_label').distinct('sub_label')
#         permission_serializer = GetPermissionResponseSchemas(permissions, many=True)
#         if permission_serializer:
#             return permission_serializer.data
#         return[]
    
#     def to_representation(self, instance):
#         data = super().to_representation(instance)

#         for field in data:
#             if data[field] is None:
#                 data[field] = ""

#         return data
    
"""ROLES LISTING API """
class GetRolesSchemas(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField('get_permissions')
    
    class Meta:
        model = Role
        fields = ['id','name','permissions']
        
    def get_permissions(self, obj):
        permissions = [name for name in obj.permissions.values_list('id', flat=True)]
        if permissions:
            return permissions
        return ""
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas
 

class RolesChoiceFieldApiSchemas(serializers.ModelSerializer):
    value = serializers.IntegerField(source='pk')
    label = serializers.CharField(source='name')

    class Meta:
        model = Role
        fields = ['value','label',]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in data.keys():
            try:
                if data[field] is None:
                    data[field] = ""
            except KeyError:
                pass
        return data
    
class GetRoleListDropdownApiResposceSchemas(serializers.ModelSerializer):
    value = serializers.IntegerField(source='pk')
    label = serializers.CharField(source='name')
    class Meta:
        model = Role
        fields = ['value','label']


"""GROUPS LISTING RESPONSE SCHEMAS"""

class GetGroupsApiRequestSerializers(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField('get_roles')
    class Meta:
        model = Group
        fields = ['pk','slug','name','roles']
        
    def get_roles(self, obj):
        roles = [name for name in obj.roles.values_list('id', flat=True)]
        return roles
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas
    
class GetGroupRolesOptionSerializer(serializers.ModelSerializer):
    
    value    =  serializers.IntegerField(source='pk')
    label    =  serializers.CharField(source='name')
    class Meta:
        model  = Permission
        fields = ['value','label']


class GetGroupDetailsApiSchema(serializers.ModelSerializer):
    
    
    roles = serializers.SerializerMethodField('get_role')
    
    class Meta:
        model = Group
        fields = ['id','name','roles']
        

    def get_role(self, obj):
        return GetGroupRolesOptionSerializer(obj.roles.all(),many=True).data



class GetPermissionsListSchema(serializers.ModelSerializer):
    
    text = serializers.CharField(source = 'name')
 
    class Meta:
        model = Permission
        fields = ['id','text']



class GetPermissionListSchema(serializers.ModelSerializer):
    
    
    children = serializers.SerializerMethodField('get_children')
    text = serializers.CharField(source = 'name')
    class Meta:
        model = Role
        fields = ['id','text','children']
        

    def get_children(self, obj):

        return GetPermissionsListSchema(obj.permissions.all(),many=True).data



class GetGroupDropdownApiSchema(serializers.ModelSerializer):
    value = serializers.CharField(source = 'id')
    label = serializers.CharField(source = 'name')
    class Meta:
        model =  Group
        fields = ['value','label']   
    




