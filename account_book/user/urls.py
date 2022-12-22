from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from user import views

# app name for reverse mapping
app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token'),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', views.UserLoginView.as_view(), name='login'),
]
