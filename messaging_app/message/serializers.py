from rest_framework import serializers
from message.models import Message
from accounts.serializers import UserValidateSerializer

"""
Serializes Message Objects to eject redundant data for responses 
"""

# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    author = UserValidateSerializer()
    target = UserValidateSerializer()

    class Meta:
        model = Message
        fields = ('author', 'target', 'content', 'timestamp',)

# Sent Messege Serializer 
class SentMessageSerializer(serializers.ModelSerializer):
    target = UserValidateSerializer()

    class Meta:
        model = Message
        fields = ('target', 'content', 'timestamp',)

# Received Message Serializer
class ReceivedMessageSerializer(serializers.ModelSerializer):
    author = UserValidateSerializer()

    class Meta:
        model = Message
        fields = ('author', 'content', 'timestamp',)

# Chat Message Serializer
class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('content', 'timestamp',)