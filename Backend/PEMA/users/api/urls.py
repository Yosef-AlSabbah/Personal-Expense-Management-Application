from django.urls import path, include

app_name = 'auth'

urlpatterns = [
    # Include Djoser’s default URLs for user management (registration, login, password reset, etc.)
    path('', include('djoser.urls')),

    # If you are using JWT authentication, include the JWT URLs for login, logout, and token management.
    path('', include('djoser.urls.jwt')),  # JWT token-based authentication
]
