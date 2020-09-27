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

# Exceptions
from exceptions.library import TargetException, OperationException, DateException

# Messsage Serializers
from message.serializers import MessageSerializer, SentMessageSerializer, ReceivedMessageSerializer
# Chat Serializer
from message.serializers import ChatSerializer
# User Serializers
from accounts.serializers import UserValidateSerializer, UserSerializer


# Message API
class MessageAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        messages = Message.objects.filter(Q(author=user) | Q(target=user)).order_by('timestamp')
        serializer = self.get_serializer(messages,many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        
        author =  request.user
        target = request.data.get('target','')

        if not target:
            raise TargetException()
        if target == author.username:
            raise OperationException()

        author_serializer = UserSerializer(author)
        target_serializer = UserValidateSerializer(data={'username' : target})
        target_serializer.is_valid(raise_exception=True)

        try:
            Block.objects.get(prevented=target_serializer.data['id'], blocked=author.id)
            raise OperationException()
        
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
        messages = Message.objects.filter(author=request.user.id).order_by('timestamp')
        serializer = self.get_serializer(messages,many=True)
        return Response(serializer.data)


# Get Received Messages API
class ReceivedMessageAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReceivedMessageSerializer

    def get(self, request, *args, **kwargs):
        messages = Message.objects.filter(target=request.user.id).order_by('timestamp')
        serializer = self.get_serializer(messages,many=True)
        return Response(serializer.data)

# Chat API
class ChatAPI(generics.GenericAPIView):
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatSerializer

    def get(self, request, target, *args, **kwargs):
        
        target_serializer = UserValidateSerializer(data={'username' : target})
        target_serializer.is_valid(raise_exception=True)

        user = request.user.id
        friend = target_serializer.data['id']

        sent = Message.objects.filter(Q(author=user) & Q(target=friend)).order_by('timestamp')
        received = Message.objects.filter(Q(author=friend) & Q(target=user)).order_by('timestamp')

        sent_serializer = self.get_serializer(sent,many=True)
        received_serializer = self.get_serializer(received, many=True)

        return Response({
            'sent' : sent_serializer.data,
            'received' : received_serializer.data
        })


# Daily Messages API
class DailyMessageAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def get(self, request, date_str, *args, **kwargs):
        
        uid = request.user.id
        date = parse_date(date_str)
        
        if date is None:
            raise DateException()
        messages = Message.objects.filter(
            (Q(author=uid) | Q(target=uid)),
            timestamp__year=date.year,
            timestamp__month=date.month,
            timestamp__day=date.day
        ).order_by('timestamp')

        serializer = self.get_serializer(messages,many=True)
        return Response(serializer.data)
