from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import UserProfileUpdateSerializer
from ..models import Profile

User = get_user_model()


class UserProfileUpdateView(UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileUpdateSerializer

    def get_object(self):
        # Get the Profile associated with the authenticated user
        return self.request.user.profile

    def perform_update(self, serializer):
        try:
            serializer.save()
        except ValidationError as e:
            raise ValidationError({"detail": "Failed to update profile. Error: " + str(e)})
