# -*- coding: utf-8 -*-
from django.contrib import admin

from apps.home.models import MainBannerImage, MainBreathVideo, TestimonialVideo


@admin.register(MainBannerImage)
class MainBannerImageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_date',
        'modified_date',
        'deleted',
        'deleted_by_cascade',
        'created_by',
        'modified_by',
        'is_active',
        'banner_image',
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


@admin.register(MainBreathVideo)
class MainBreathVideoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_date',
        'modified_date',
        'deleted',
        'deleted_by_cascade',
        'created_by',
        'modified_by',
        'is_active',
        'main_video_url',
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


@admin.register(TestimonialVideo)
class TestimonialVideoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_date',
        'modified_date',
        'deleted',
        'deleted_by_cascade',
        'created_by',
        'modified_by',
        'is_active',
        'testimonial_url',
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
