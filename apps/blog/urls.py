from django.contrib import admin
from django.urls import path, re_path, include
from . import views

urlpatterns = [

    re_path(r'^blog/', include([
        path('create-or-update-blog', views.CreateOrUpdateBlogAPIView.as_view()),
        path('list-blog', views.GetBlogListAPIView.as_view()),
        path('detail-blog', views.GetBlogDetailedAPIView.as_view()),
        path('detail-blog-web', views.GetBlogDetailedWebAPIView.as_view()),
        path('delete-blog', views.DeleteBlogAPIView.as_view()),
    ])),

    re_path(r'^service/', include([
        path('create-or-update-service', views.CreateOrUpdateServiceURLAPIView.as_view()),
        path('list-service', views.GetServiceURLListAPIView.as_view()),
        path('detail-service', views.GetServiceURLDetailedAPIView.as_view()),
        path('delete-service', views.DeleteServiceAPIView.as_view()),
    ])),

    re_path(r'^patient-stories/', include([
        path('create-or-update-patient-stories', views.CreateOrUpdatePatientStoriesAPIView.as_view()),
        path('list-patient-stories', views.GetPatientStoriesListAPIView.as_view()),
        path('detail-patient-stories', views.GetPatientStoriesDetailedAPIView.as_view()),
        path('delete-patient-stories', views.DeletePatientStoriesAPIView.as_view()),
    ])),

    re_path(r'^gallery/', include([
        path('create-or-update-gallery', views.CreateOrUpdateGalleryAPIView.as_view()),
        path('list-gallery', views.GetGalleryListAPIView.as_view()),
        path('detail-gallery', views.GetGalleryDetailedAPIView.as_view()),
        path('delete-gallery', views.DeleteGalleryAPIView.as_view()),
    ])),

    re_path(r'^award/', include([
        path('create-or-update-award', views.CreateOrUpdateAwardAPIView.as_view()),
        path('list-award', views.GetAwardListAPIView.as_view()),
        path('detail-award', views.GetAwardDetailedAPIView.as_view()),
        path('delete-award', views.DeleteAwardAPIView.as_view()),
    ])),

    re_path(r'^event/', include([
        path('create-or-update-event', views.CreateOrUpdateEventAPIView.as_view()),
        path('list-event', views.GetEventListAPIView.as_view()),
        path('detail-event', views.GetEventDetailedAPIView.as_view()),
        path('delete-event', views.DeleteEventAPIView.as_view()),
    ])),

    re_path(r'^subscription/', include([
        path('create-or-update-subscription', views.CreateOrUpdateSubscriptionAPIView.as_view()),
        path('unsubscribe', views.UnSubScriptionAPIView.as_view()),
        # path('list-subscription', views.GetEventListAPIView.as_view()),
    ])),

    re_path(r'^communication/', include([
        path('create-or-update-communication', views.CreateOrUpdateCommunicationAPIView.as_view()),
        # path('list-subscription', views.GetEventListAPIView.as_view()),
    ])),
]