from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ AUTH URLS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Include Djoser’s default URLs for user management (registration, login, password reset, etc.)
    path('', include('djoser.urls')),

    # If you are using JWT authentication, include the JWT URLs for login, logout, and token management.
    path('', include('djoser.urls.jwt')),  # JWT token-based authentication

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ADMIN SITE URLS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    path('admin/', admin.site.urls),

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ API V1 URLS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # All API endpoints are organized under 'api/v1/'
    path('api/v1/', include('api.urls', namespace='api')),
]
