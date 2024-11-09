from django.contrib.auth import get_user_model
from rest_framework import serializers
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
        fields = ['profile_pic']

    def validate_profile_pic(self, value):
        # Limit file size to 2MB
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("Profile picture size should not exceed 2MB.")
        return value


class UserProfileUpdateSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'profile_pic']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        # Update user data
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        # Update profile data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    def validate(self, attrs):
        return attrs
