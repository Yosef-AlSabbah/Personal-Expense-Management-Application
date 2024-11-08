from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin site URLs
    path('admin/', admin.site.urls),

    # Include API URLs under the 'api/' path
    path('api/', include('api.urls'), namespace='api'),
]
