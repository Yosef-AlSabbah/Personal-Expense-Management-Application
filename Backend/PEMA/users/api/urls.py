from django.urls import path

from users.api.views import (
    UserViewSet,
    TokenDestroyView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

app_name = 'auth'

# Define actions for UserViewSet
user_create = UserViewSet.as_view({'post': 'create'})
user_activate = UserViewSet.as_view({'post': 'activation'})
user_set_password = UserViewSet.as_view({'post': 'set_password'})
user_reset_password = UserViewSet.as_view({'post': 'reset_password'})
user_reset_password_confirm = UserViewSet.as_view({'post': 'reset_password_confirm'})

# Define 'me' endpoint with all desired HTTP methods mapped to 'me' action
user_me = UserViewSet.as_view({
    'get': 'me',
    'put': 'me',
    'patch': 'me',
    'delete': 'me',
})

urlpatterns = [
    # User registration
    path('register/', user_create, name='register'),
    # User activation
    path('activate/', user_activate, name='activate'),
    # Set password
    path('set-password/', user_set_password, name='set_password'),
    # Reset password
    path('reset-password/', user_reset_password, name='reset_password'),
    # Confirm password reset
    path('reset-password-confirm/', user_reset_password_confirm, name='reset_password_confirm'),
    # JWT token endpoints
    path('token/obtain/', TokenObtainPairView.as_view(), name='jwt-create'),
    path('token/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='jwt-verify'),
    path('token/destroy/', TokenDestroyView.as_view(), name='jwt-destroy'),
    # Current authenticated user with multiple methods
    path('me/', user_me, name='current_user'),
]
