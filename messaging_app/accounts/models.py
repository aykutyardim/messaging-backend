from django.contrib.auth.models import User
from django.db import models

# Blocking Model
class Block(models.Model):
    prevented = models.ForeignKey(User, related_name='prevented_blocks', on_delete=models.CASCADE)
    blocked = models.ForeignKey(User, related_name='blocked_blocks', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('prevented' , 'blocked',)

# Login Activity Model
class LoginActivity(models.Model):
    SUCCESS = 'S'
    FAILED = 'F'
    LOGIN_STATUS = ((SUCCESS, 'Success'),(FAILED, 'Failed'))

    login_IP = models.GenericIPAddressField(null=True, blank=True)
    login_username = models.CharField(max_length=50, null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=1, choices=LOGIN_STATUS, default=SUCCESS)
    timestamp = models.DateTimeField(auto_now_add=True)