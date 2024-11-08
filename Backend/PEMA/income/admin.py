from django.contrib import admin
from .models import Income


# Registering the Income model in the admin interface
@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    # Fields to display in the list view for quick overview
    list_display = ('user', 'amount', 'date', 'last_updated', 'description')

    # Search functionality for the admin interface
    search_fields = ('user__name', 'amount', 'description')

    # Filter options to narrow down results quickly
    list_filter = ('user', 'date', 'last_updated')

    # Ordering income entries by date, most recent first
    ordering = ['-date']

    # Fields to show when adding/editing an income entry
    fields = ('user', 'amount', 'description')
