from rest_framework import serializers
from message.models import Message
from accounts.serializers import UserValidateSerializer

class MessageSerializer(serializers.ModelSerializer):
    author = UserValidateSerializer()
    target = UserValidateSerializer()

    class Meta:
        model = Message
        fields = ('author', 'target', 'content', 'timestamp',)

class SentMessageSerializer(serializers.ModelSerializer):
    target = UserValidateSerializer()

    class Meta:
        model = Message
        fields = ('target', 'content', 'timestamp',)

class ReceivedMessageSerializer(serializers.ModelSerializer):
    author = UserValidateSerializer()

    class Meta:
        model = Message
        fields = ('author', 'content', 'timestamp',)

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('content', 'timestamp',)