from django.contrib import admin
from .models import Category, Expense


# Registering the Category model in the admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('name', 'description')

    # Add search capability for these fields
    search_fields = ('name', 'description')

    # Filter options for quick navigation
    list_filter = ('name',)


# Registering the Expense model in the admin
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('user', 'amount', 'date', 'category', 'description')

    # Enable searching by these fields
    search_fields = ('user__username', 'amount', 'category__name', 'description')

    # Filtering options to narrow down results
    list_filter = ('user', 'category', 'date')

    # Order expenses by date, newest first
    ordering = ['-date']

    # Fields to show when adding or editing an expense
    fields = ('user', 'amount', 'category', 'description')

    # Exclude the 'date' field, as it is automatically set
    exclude = ('date',)