from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from record.views import redirect_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(
        [
            path('user/', include('user.urls')),
            path('record/', include('record.urls')),
        ]
    )
    ),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'),
         name='api-docs'),

    path('<new_url>', redirect_url)
]
