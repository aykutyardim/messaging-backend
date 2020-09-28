# Requirements
from rest_framework import generics, permissions, serializers
from rest_framework.response import Response
from knox.models import AuthToken
from django.utils.dateparse import parse_date
from django.core.exceptions import ObjectDoesNotExist

# Models
from message.models import Message
from accounts.models import Block
from django.contrib.auth.models import User
from django.db.models import Q

# Messsage Serializers
from message.serializers import MessageSerializer, SentMessageSerializer, ReceivedMessageSerializer
# Chat Serializer
from message.serializers import ChatSerializer
# User Serializers
from accounts.serializers import UserValidateSerializer, UserSerializer

# Custom Exceptions
from exceptions.library import TargetException, OperationException, DateException

# Message API
class MessageAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def get(self, request, *args, **kwargs):

        # Get user messages 
        user = request.user
        messages = Message.objects.filter(Q(author=user) | Q(target=user)).order_by('timestamp')
        
        # Serialize user messages
        serializer = self.get_serializer(messages,many=True)
        
        # Return serialized messages
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        
        # Get request data
        author =  request.user
        target = request.data.get('target','')

        # Check body
        if not target:
            raise TargetException()
        if target == author.username:
            raise OperationException()
        
        # Serialize client
        author_serializer = UserSerializer(author)
        
        # Serialize & Validate request data
        target_serializer = UserValidateSerializer(data={'username' : target})
        target_serializer.is_valid(raise_exception=True)

        # Check Client Blocked by Target case
        try:
            Block.objects.get(prevented=target_serializer.data['id'], blocked=author.id)
            raise OperationException()
        
        # Validate & Save message
        except ObjectDoesNotExist:
            data = request.data
            data['target'] = target_serializer.data
            data['author'] = author_serializer.data
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

# Get Sent Messages API
class SentMessageAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SentMessageSerializer

    def get(self, request, *args, **kwargs):
        
        # Get & Serialize sent messages
        messages = Message.objects.filter(author=request.user.id).order_by('timestamp')
        serializer = self.get_serializer(messages,many=True)
        return Response(serializer.data)


# Get Received Messages API
class ReceivedMessageAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReceivedMessageSerializer

    def get(self, request, *args, **kwargs):

        # Get & Serialize received messages
        messages = Message.objects.filter(target=request.user.id).order_by('timestamp')
        serializer = self.get_serializer(messages,many=True)
        return Response(serializer.data)

# Chat API
class ChatAPI(generics.GenericAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatSerializer

    def get(self, request, target, *args, **kwargs):
        
        # Validate target data
        target_serializer = UserValidateSerializer(data={'username' : target})
        target_serializer.is_valid(raise_exception=True)

        # Set users
        user = request.user.id
        friend = target_serializer.data['id']

        # Get Chat Messages
        sent = Message.objects.filter(Q(author=user) & Q(target=friend)).order_by('timestamp')
        received = Message.objects.filter(Q(author=friend) & Q(target=user)).order_by('timestamp')

        # Serialize Chat Messages
        sent_serializer = self.get_serializer(sent,many=True)
        received_serializer = self.get_serializer(received, many=True)

        # Return Chat
        return Response({
            'sent' : sent_serializer.data,
            'received' : received_serializer.data
        })


# Daily Messages API
class DailyMessageAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def get(self, request, date_str, *args, **kwargs):

        # Get request data        
        uid = request.user.id
        date = parse_date(date_str)
        
        # Check params
        if date is None:
            raise DateException()

        #Get Daily Messages 
        messages = Message.objects.filter(
            (Q(author=uid) | Q(target=uid)),
            timestamp__year=date.year,
            timestamp__month=date.month,
            timestamp__day=date.day
        ).order_by('timestamp')

        # Serialize & Return Messages
        serializer = self.get_serializer(messages,many=True)
        return Response(serializer.data)
