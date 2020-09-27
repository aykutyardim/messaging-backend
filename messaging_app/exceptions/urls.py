from django.urls import path
from exceptions.api import ExceptionAPI

urlpatterns = [
    path('api/exception', ExceptionAPI.as_view())
]