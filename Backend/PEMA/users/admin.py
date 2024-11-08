from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin view for the Profile model.
    """
    list_display = ('user', 'balance', 'date_created')
    search_fields = ('user__name', 'user__email')
    readonly_fields = ('user', 'balance', 'date_created')

    def has_change_permission(self, request, obj=None):
        """
        Restricts the change permission to make the profile unchangeable from the admin dashboard.
        """
        return False
