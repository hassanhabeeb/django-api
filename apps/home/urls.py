from django.contrib import admin
from django.urls import path, re_path, include
from . import views

urlpatterns = [

    re_path(r'^main-banner/', include([
        path('create-or-update-main-banner', views.CreateOrUpdateMainBannerImageAPIView.as_view()),
        path('list-main-banner', views.GetMainBannerImageListAPIView.as_view()),
        path('detail-main-banner', views.GetMainBannerImageDetailedAPIView.as_view()),
        path('delete-main-banner', views.DeleteMainBannerImageAPIView.as_view()),
    ])),

    re_path(r'^breath-video/', include([
        path('create-or-update-breath-video', views.CreateOrUpdateMainBreathVideoAPIView.as_view()),
        path('list-breath-video', views.GetMainBreathVideoListAPIView.as_view()),
        path('detail-breath-video', views.GetMainBreathVideoDetailedAPIView.as_view()),
        path('delete-breath-video', views.DeleteMainBreathVideoAPIView.as_view()),
    ])),

    re_path(r'^testimonial-video/', include([
        path('create-or-update-testimonial', views.CreateOrUpdateTestimonialVideoAPIView.as_view()),
        path('list-testimonial', views.GetTestimonialVideoListAPIView.as_view()),
        path('detail-testimonial', views.GetTestimonialVideoDetailedAPIView.as_view()),
        path('delete-testimonial', views.DeleteTestimonialVideoAPIView.as_view()),
    ])),

]