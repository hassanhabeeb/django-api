from rest_framework import serializers
from apps.user.models import Users
from django.contrib.auth.models import Permission




class LoginResponseSchema(serializers.ModelSerializer):
    permissions       = serializers.SerializerMethodField('get_permissions')
    group             = serializers.SerializerMethodField('get_groups')
 
    phonenumber       = serializers.SerializerMethodField('get_phonenumber')
    # active_choices = serializers.
    # selected_branch_name    = serializers.SerializerMethodField('get_branch_name')

    
    
    class Meta:
        model = Users
        fields = [
            "id",
           
            "email",
            "name",
            "username",
            "first_name",
            "last_name",
           
            "phonenumber",
            "is_admin",
            "is_active",
            "is_verified",
            "is_superuser",
            "is_staff",
            'permissions',
            'group',
            # 'selected_branch',
            # 'selected_branch_name',
        ]

    def get_permissions(self, data):
            perm_l = []
            for group in data.user_groups.all():
                role = group.roles.all().values_list('id', flat=True)
                perm_l.extend(Permission.objects.filter(group__in=role).values_list('codename', flat=True))
            return perm_l
    

    


    def get_groups(self, data):
        groups = data.user_groups.all()
        return [{'id': group.id, 'name': group.name} for group in groups]
    
    
        
    def get_phonenumber(self,data):
        return data.phonenumber if data.phonenumber else None
    
    # def get_branch_name(self, obj):
    #     return obj.selected_branch.branch_name if obj.selected_branch else None
    
    
class UserAdminForgotPasswordResponseSchema(serializers.ModelSerializer):
    user_email = serializers.EmailField(required=True)
    class Meta:
        model = Users
        fields = ['user_email']