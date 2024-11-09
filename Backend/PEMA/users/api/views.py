from django.contrib.auth import get_user_model
from rest_framework.generics import UpdateAPIView

from .serializers import UserProfileUpdateSerializer
from ..models import Profile

User = get_user_model()


class UserProfileUpdateView(UpdateAPIView):
    queryset = Profile.objects.all()  # Use Profile as the queryset
    serializer_class = UserProfileUpdateSerializer

    def get_object(self):
        # Get the Profile associated with the authenticated user
        return self.request.user.profile

