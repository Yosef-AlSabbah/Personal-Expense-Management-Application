from django.urls import path, include

# Application namespace to avoid conflicts
app_name = 'api'

urlpatterns = [
    # Authentication URLs
    # These include JWT token management routes under 'auth/'
    path('users/', include('users.api.urls', namespace='auth')),

    # Expenses URLs
    # Organized under 'expenses/' with a specific namespace
    path('expenses/', include('expenses.api.urls', namespace='expenses')),

    # Income URLs
    # Organized under 'income/' with a specific namespace
    path('income/', include('income.api.urls', namespace='income')),

    # Reports URLs
    # Organized under 'reports/' with a specific namespace
    path('reports/', include('reports.api.urls', namespace='reports')),
]