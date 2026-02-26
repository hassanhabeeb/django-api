# admin.py

from django.contrib.admin import AdminSite
# from .models import Users

class Replica1AdminSite(AdminSite):
    site_header = 'Replica 1 Admin'
    site_title = 'Replica 1 Admin'
    index_title = 'Replica 1 Administration'

class Replica2AdminSite(AdminSite):
    site_header = 'Replica 2 Admin'
    site_title = 'Replica 2 Admin'
    index_title = 'Replica 2 Administration'

replica1_admin_site = Replica1AdminSite(name='replica1_admin')
replica2_admin_site = Replica2AdminSite(name='replica2_admin')

# Register your models here
from django.contrib import admin


class UsersReplica1Admin(admin.ModelAdmin):
    list_display = ('username', 'email', 'replica_db')
    # Add any other customizations here

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(replica_db='replica_1')

class UsersReplica2Admin(admin.ModelAdmin):
    list_display = ('username', 'email', 'replica_db')
    # Add any other customizations here

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(replica_db='replica_2')

