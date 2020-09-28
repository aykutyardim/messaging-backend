from django.contrib.auth.models import User
from django.db import models

# Messages Model
class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    target = models.ForeignKey(User, related_name='target_messages', on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)