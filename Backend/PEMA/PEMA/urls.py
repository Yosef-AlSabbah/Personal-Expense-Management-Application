from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

# Define schema view for Swagger and ReDoc
schema_view = get_schema_view(
    openapi.Info(
        title="Personal Expense Management Backend API Documentation",
        default_version="v1",
        description="API documentation for Personal Expense Management",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="yalsabbah@students.iugaza.edu.ps"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,

    # Allow only admins access to the documentation
    permission_classes=[AllowAny],
)

urlpatterns = [
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ AUTH URLS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ADMIN SITE URLS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    path('admin/', admin.site.urls),

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ API V1 URLS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    path('api/v1/', include('api.urls', namespace='api')),

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ SWAGGER URLS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
