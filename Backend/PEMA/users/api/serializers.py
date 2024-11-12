from django.contrib.auth import get_user_model
from django.db import transaction
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ..models import Profile

User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    """
    Serializer for creating a new user account.
    Includes both User and Profile fields needed for registration.
    """

    profile_pic = serializers.ImageField(
        required=False,
        help_text="Upload a profile picture (max size 2MB).",
    )

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'phone_number', 'profile_pic')
        extra_kwargs = {
            'username': {'help_text': "User's username MUST be UNIQUE."},
            'email': {'help_text': "User's email address MUST be UNIQUE."},
            'first_name': {'help_text': "User's first name."},
            'last_name': {'help_text': "User's last name."},
            'phone_number': {'help_text': "User's phone number."}
        }

    def validate_profile_pic(self, value):
        """Validate that the uploaded profile picture does not exceed 2MB."""
        if value and value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Profile picture size should not exceed 2MB.")
        return value

    def create(self, validated_data):
        """
        Creates a new user along with their profile.
        Profile is created automatically by signal, with custom error handling for profile creation issues.
        """
        profile_pic = validated_data.pop('profile_pic', None)

        try:
            with transaction.atomic():
                # Create the user, triggering the signal that auto-creates the profile
                user = User.objects.create_user(**validated_data)

                # Update profile picture if provided and profile creation was successful
                if profile_pic:
                    # Attach profile_pic to the automatically created Profile instance
                    user.profile.profile_pic = profile_pic
                    user.profile.save()

            return user

        except Exception as e:
            # User was created, but there was an issue with profile setup
            raise serializers.ValidationError({
                'profile': f"User created, but profile setup encountered an issue: {str(e)}"
            })


class UserDetailSerializer(ModelSerializer):
    """
    Serializer for retrieving user information.
    Excludes sensitive fields like password for security.
    """

    class Meta:
        model = User
        ref_name = "UserDetailSerializer"
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number']
        extra_kwargs = {
            'username': {'help_text': "User's username."},
            'email': {'help_text': "User's email address."},
            'first_name': {'help_text': "User's first name."},
            'last_name': {'help_text': "User's last name."},
            'phone_number': {'help_text': "User's phone number."}
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

    user = UserDetailSerializer(help_text="User details (username, email, first name, last name, and phone number).")
    profile_pic = serializers.ImageField(
        help_text="Upload a profile picture (max size 2MB).", required=False
    )

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

        # Update profile_pic only if provided
        if 'profile_pic' in validated_data:
            instance.profile_pic = validated_data['profile_pic']

        # Update other profile fields if needed
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    def validate(self, attrs):
        """Ensure only the owner of the profile can update it."""
        request = self.context.get('request')
        if request and request.user != self.instance.user:
            raise serializers.ValidationError("You do not have permission to update this profile.")
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for adding additional claims to the JWT token.
    Adds the 'is_verified' status of the user to the token payload.
    """

    @classmethod
    def get_token(cls, user):
        # Call the superclass method to get the default token
        token = super().get_token(user)

        # Add a custom claim to the token: 'is_verified' status of the user
        token['is_verified'] = user.is_verified
        return token
