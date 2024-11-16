from django.urls import path, include
# Define schema view for Swagger and ReDoc
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.permissions import AllowAny

# API schema view using drf-spectacular
schema_view = SpectacularAPIView.as_view()

# Swagger documentation view
swagger_view = SpectacularSwaggerView.as_view(
    url_name='schema',
    # permission_classes=[IsAdminUser],  # Allow only admins access to the documentation
    permission_classes=[AllowAny],
)

# Redoc documentation view (optional)
redoc_view = SpectacularRedocView.as_view(
    url_name='schema',
    # permission_classes=[IsAdminUser],  # Allow only admins access to the documentation
    permission_classes=[AllowAny],
)
# Application namespace to avoid conflicts
app_name = 'api'

urlpatterns = [
    # Authentication URLs
    # These include JWT token management routes under 'auth/'
    path('auth/', include('users.api.urls', namespace='auth')),

    # Expenses URLs
    # Organized under 'expenses/' with a specific namespace
    path('expenses/', include('expenses.api.urls', namespace='expenses')),

    # Income URLs
    # Organized under 'income/' with a specific namespace
    path('income/', include('income.api.urls', namespace='income')),

    # Reports URLs
    # Organized under 'reports/' with a specific namespace
    path('reports/', include('reports.api.urls', namespace='reports')),

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ SWAGGER URLS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # OpenAPI Schema endpoint
    path('schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI endpoint
    path('swagger/', SpectacularSwaggerView.as_view(url_name='api:schema'), name='swagger-ui'),

    # ReDoc UI endpoint
    path('redoc/', SpectacularRedocView.as_view(url_name='api:schema'), name='redoc'),
]
