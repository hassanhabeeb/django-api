"""
URL configuration for breathline project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.views.generic import RedirectView
from django.conf import settings

from .admin import replica1_admin_site, replica2_admin_site

schema_view = get_schema_view(
    openapi.Info(
        title="Breathline API",
        default_version='v1',
        description=(
            "An online platform for a breath-focused medical clinic, providing "
            "information about services, expert articles, wellness tips, and "
            "breathing-related health resources. The website also allows visitors "
            "to make service enquiries and connect with the clinic for consultations."
        ),
        terms_of_service="",
        contact=openapi.Contact(email="anjana@aventusinformatics.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Redirect root → Swagger docs
    path('', RedirectView.as_view(url='api/docs/')),

    re_path(r'^api/', include([
        path('user/', include('apps.user.urls')),
        path('auth/', include('apps.authentication.urls')),
        path('blog/', include('apps.blog.urls')),
        path('home/', include('apps.home.urls')),

        re_path(r'^docs/', include([
            path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
            path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        ])),
    ])),
]

# NOTE: In production with WhiteNoise, static files are served automatically
# by the WhiteNoiseMiddleware — no extra URL patterns needed.
# staticfiles_urlpatterns() and static() only work in DEBUG=True mode anyway.