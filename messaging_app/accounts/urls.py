# Requirements
from django.urls import path, include
from knox import views as knox_views

# User API
from .api import UserAPI, RegisterAPI, LoginAPI, BlockAPI

# Admin API
from accounts.api import LoginActivityAPI

urlpatterns = [
    path('api/auth', include('knox.urls')),
    path('api/auth/register', RegisterAPI.as_view()),
    path('api/auth/login', LoginAPI.as_view()),
    path('api/auth/user', UserAPI.as_view()),
    path('api/auth/block', BlockAPI.as_view()),
    path('api/auth/loginactivity', LoginActivityAPI.as_view()),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout')
]