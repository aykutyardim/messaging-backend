# Requirements
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status

# Exceptions
from exceptions.library import BlockedException, OperationException
from django.core.exceptions import ObjectDoesNotExist

# Models
from knox.models import AuthToken
from django.contrib.auth.models import User
from accounts.models import Block, LoginActivity

# User Serializers
from accounts.serializers import UserSerializer, RegisterSerializer, LoginSerializer, UserValidateSerializer
# Block Serializers
from accounts.serializers import GetBlockSerializer, BlockSerializer
# Activity Serializers
from accounts.serializers import LoginActivitySerializer


# Get User API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        
        # Set email empty, If not given 
        data = request.data
        email = data.get('email','')
        data['email'] = email

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user" : UserSerializer(user, context=self.get_serializer_context()).data,
            "token" : AuthToken.objects.create(user)[1]
        })
        
# Login API
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user= serializer.validated_data
        return Response({
            "user" : UserSerializer(user, context=self.get_serializer_context()).data,
            "token" : AuthToken.objects.create(user)[1]
        })

# Block API
class BlockAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BlockSerializer

    def get(self, request, *args, **kwargs):
        blocks = Block.objects.filter(prevented=request.user.id).order_by('timestamp')
        serializer = GetBlockSerializer(blocks,many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        
        prevented = request.user
        blocked = request.data.get('blocked','')
        
        if not blocked:
            raise BlockedException()
        if blocked == prevented.username:
            raise OperationException()    
        
        prevented_serializer = UserSerializer(prevented)
        blocked_serializer = UserValidateSerializer(data={'username' : blocked})
        blocked_serializer.is_valid(raise_exception=True)

        data = {}
        data['prevented'] = prevented_serializer.data
        data['blocked'] = blocked_serializer.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):

        blocked = request.data.get('blocked','')
        if not blocked:
            raise BlockedException()

        blocked_serializer = UserValidateSerializer(data={'username' : blocked})
        blocked_serializer.is_valid(raise_exception=True)
        
        try:
            block = Block.objects.get(prevented=request.user.id, blocked=blocked_serializer.data['id'])
            block.delete()
            return Response([])
        except ObjectDoesNotExist:
            raise OperationException()

# Get User Acticity API
class LoginActivityAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = LoginActivitySerializer

    def get(self, request, *args, **kwargs):
        activities = LoginActivity.objects.all()
        serializer = self.get_serializer(activities,many=True)
        return Response(serializer.data)