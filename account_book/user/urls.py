from django.urls import path

from user import views

# app name for reverse mapping
app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token'),
    path('token/refresh', views.CustomTokenRefreshView.as_view(),
         name='token_refresh'),
    path('token/verify', views.CustomTokenVerifyView.as_view(), name='token_verify'),
]
