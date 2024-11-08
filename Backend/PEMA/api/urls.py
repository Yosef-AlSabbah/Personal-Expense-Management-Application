from django.urls import path, include

# Set an application namespace for the API to avoid URL naming conflicts.
app_name = 'api'

urlpatterns = [
    # Authentication URLs
    # This includes user authentication and JWT token management routes under the 'auth/' path.
    # Contains all necessary authentication endpoints (e.g., registration, login, password reset).
    path('auth/', include('users.api.urls')),

    # Expenses URLs
    # Uses the 'expenses' namespace for organized URL naming.
    path('expenses/', include('expenses.api.urls', namespace='expenses')),

    # Income URLs
    # Uses the 'income' namespace to keep URL names unique.
    path('income/', include('income.api.urls', namespace='income')),

    # Reports URLs
    # Uses the 'reports' namespace for clear and unique URL naming.
    path('reports/', include('reports.api.urls', namespace='reports')),
]
