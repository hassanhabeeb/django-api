# -*- coding: utf-8 -*-
from django.contrib import admin

from apps.blog.models import Blog, Service, PatientStories, Gallery, Award, Event, Subscription, Communication


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_date',
        'modified_date',
        'deleted',
        'deleted_by_cascade',
        'created_by',
        'modified_by',
        'is_active',
        'title',
        'sub_title',
        'slug',
        'description',
        'author',
        'blog_image',
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


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_date',
        'modified_date',
        'deleted',
        'deleted_by_cascade',
        'created_by',
        'modified_by',
        'is_active',
        'service_category',
        'service_video_url',
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


@admin.register(PatientStories)
class PatientStoriesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_date',
        'modified_date',
        'deleted',
        'deleted_by_cascade',
        'created_by',
        'modified_by',
        'is_active',
        'name',
        'description',
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
    search_fields = ('name',)


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_date',
        'modified_date',
        'deleted',
        'deleted_by_cascade',
        'created_by',
        'modified_by',
        'is_active',
        'image',
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


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_date',
        'modified_date',
        'deleted',
        'deleted_by_cascade',
        'created_by',
        'modified_by',
        'is_active',
        'award_image',
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


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_date',
        'modified_date',
        'deleted',
        'deleted_by_cascade',
        'created_by',
        'modified_by',
        'is_active',
        'event_image',
        'description',
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


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_date',
        'modified_date',
        'deleted',
        'deleted_by_cascade',
        'created_by',
        'modified_by',
        'is_active',
        'email',
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


@admin.register(Communication)
class CommunicationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_date',
        'modified_date',
        'deleted',
        'deleted_by_cascade',
        'created_by',
        'modified_by',
        'is_active',
        'name',
        'email',
        'phonenumber',
        'service_category',
        'message',
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
    search_fields = ('name',)
