from django.urls import path
from . import views


urlpatterns = [
    
    path('login', views.LoginApiView.as_view()),
    path('logout', views.LogoutApiView.as_view()),
    path('forgot-password', views.UserAdminForgotPasswordAPIView.as_view()),
    path('reset-password', views.AdminPasswordResetConfirmView.as_view()),
    path('register/', views.CreateOrUpdateUserApiView.as_view(), name='user-register'),
    # path('permission-listing',views.PermissionListing.as_view())

]