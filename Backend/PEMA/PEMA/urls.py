from django.contrib import admin
from django.urls import path, include


from users.views import activate_account



urlpatterns = [
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ADMIN SITE URLS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    path('admin/', admin.site.urls),

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ API V1 URLS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    path('api/v1/', include('api.urls', namespace='api')),


    # ━━━━━━━━━━━━━━━━━━━━━━━ TEMP URL UNTIL FRONT-END IS AVAILABLE ━━━━━━━━━━━━━━━━━━━━━━━━
    path('activate/<str:uid>/<str:token>/', activate_account, name='activate_account'),
]
