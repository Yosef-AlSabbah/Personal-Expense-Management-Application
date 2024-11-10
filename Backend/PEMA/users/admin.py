from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth import get_user_model

from .models import Profile

User = get_user_model()


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    """
    Admin view for the Profile model with limited edit permissions.
    """
    list_display = ('user', 'balance', 'date_created')
    search_fields = ('user__username', 'user__email')  # Use 'username' and 'email' instead of 'name'

    readonly_fields = ('balance', 'date_created')  # Make balance and date_created read-only

    def get_form(self, request, obj=None, **kwargs):
        """Customize form to limit user choices and enforce creation-only permissions."""
        form = super().get_form(request, obj, **kwargs)
        if obj is None:
            # Restrict user choices to those without a profile only during creation
            form.base_fields['user'].queryset = User.objects.filter(profile__isnull=True)
        else:
            # Make the user field read-only when viewing an existing profile
            self.readonly_fields = ('user', 'balance', 'date_created')
        return form

    def has_change_permission(self, request, obj=None):
        """
        Allow profile creation but restrict editing after creation.
        """
        if obj is not None:
            return False  # Disable editing of existing profiles
        return True
