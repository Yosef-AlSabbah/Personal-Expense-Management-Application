from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from ..models import Profile

User = get_user_model()


class UserSerializer(ModelSerializer):
    """Serializer for user information, used within profile-related serializers."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        extra_kwargs = {
            'first_name': {'help_text': "User's first name."},
            'last_name': {'help_text': "User's last name."},
            'email': {'help_text': "User's email address."}
        }


class ProfileSerializer(ModelSerializer):
    """Serializer for retrieving the user's profile with a profile picture."""

    profile_pic = serializers.ImageField(
        help_text="Upload a profile picture (max size 2MB)."
    )

    class Meta:
        model = Profile
        fields = ['profile_pic']

    def validate_profile_pic(self, value):
        """Validate that the uploaded profile picture does not exceed 2MB."""
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Profile picture size should not exceed 2MB.")
        return value


class UserProfileUpdateSerializer(ModelSerializer):
    """Serializer for updating user profile and related user information."""

    user = UserSerializer(help_text="User details (first name, last name, and email).")

    class Meta:
        model = Profile
        fields = ['user', 'profile_pic']

    def update(self, instance, validated_data):
        """Update user information along with profile data."""
        user_data = validated_data.pop('user', {})

        # Update user details
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        # Update profile details
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    def validate(self, attrs):
        """Custom validation logic for updating the profile."""
        return attrs
