from django.contrib import admin
from django.urls import path, include

from record.views import redirect_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/', include('user.urls')),
    path('api/v1/record/', include('record.urls')),
    path('<new_url>', redirect_url)
]
