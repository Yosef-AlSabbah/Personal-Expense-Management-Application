from django.urls import path

from .views import UserProfileUpdateView

app_name = 'users'

urlpatterns = [
    # Endpoint for updating the profile of the authenticated user
    path('profile/', UserProfileUpdateView.as_view(), name='profile-update'),
]
