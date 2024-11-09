from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from ..models import Profile

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        # Balance is excluded
        fields = ['profile_pic']


class UserProfileUpdateSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'profile_pic']

    def update(self, instance, validated_data):
        # Separate out user data from the profile data
        user_data = validated_data.pop('user', {})

        # Update user fields
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        # Update profile fields (e.g., profile_pic)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance