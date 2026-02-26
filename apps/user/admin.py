
    
    
DATABASE_PORT: 5432
REPLICA_1_PORT: 5432
REPLICA_2_PORT: 5432
# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import ErrorLog, Users, GeneratedAccessToken

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_date',
        'modified_date',
        'email',
        'username',
        'slug',
        'date_joined',
        'last_login',
        'last_logout',
        'last_active',
        'last_password_reset',
        'is_verified',
        'is_admin',
        'is_staff',
        'is_superuser',
        'is_logged_in',
        'failed_login_attempts',
        'is_active',
        'is_password_reset_required',
        'name',
        'replica_db',
    )
    list_filter = (
        'created_date',
        'modified_date',
        'date_joined',
        'last_login',
        'last_logout',
        'last_active',
        'last_password_reset',
        'is_verified',
        'is_admin',
        'is_staff',
        'is_superuser',
        'is_logged_in',
        'is_active',
        'is_password_reset_required',
    )
    exclude = ['password']
   
   


@admin.register(GeneratedAccessToken)
class GeneratedAccessTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_date', 'modified_date', 'token', 'user')
    list_filter = ('created_date', 'modified_date', 'user')





@admin.register(ErrorLog)
class ErrorLogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_date',
        'modified_date',
        'deleted',
        'deleted_by_cascade',
        'created_by',
        'modified_by',
        'is_active',
        'error_message',
        'user_id',
    )
    list_filter = (
        'created_date',
        'modified_date',
        'deleted',
        'deleted_by_cascade',
        'created_by',
        'modified_by',
        'is_active',
    )



