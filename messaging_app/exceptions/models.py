from django.db import models
from django.contrib.auth.models import User

class ExceptionModel(models.Model):

    username = models.CharField(max_length=50, blank=True, null=True)
    user_IP = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    request_method = models.CharField(max_length=30, blank=True, null=True)
    request_path = models.CharField(max_length=255, blank=True, null=True)
    status_code = models.CharField(max_length=50, blank=True, null=True)
    error_code = models.CharField(max_length=50, blank=True, null=True)
    error_codes = models.JSONField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)