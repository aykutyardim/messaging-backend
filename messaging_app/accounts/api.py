# Requirements
from rest_framework import generics, permissions
from rest_framework.response import Response

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


# User API
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        
        # Get email
        data = request.data
        email = data.get('email','')
        data['email'] = email

        # Validate register request data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Save & Return user
        user = serializer.save()
        return Response({
            "user" : UserSerializer(user, context=self.get_serializer_context()).data,
            "token" : AuthToken.objects.create(user)[1]
        })
        
# Login API
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        
        # Validate credentials
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Return User
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
        
        # Serialize blocking data
        blocks = Block.objects.filter(prevented=request.user.id).order_by('timestamp')
        serializer = GetBlockSerializer(blocks,many=True)
        
        # Return Block list
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        
        # Get request data
        prevented = request.user
        blocked = request.data.get('blocked','')
        
        # Check body
        if not blocked:
            raise BlockedException()
        if blocked == prevented.username:
            raise OperationException()    
        
        # Serialize client
        prevented_serializer = UserSerializer(prevented)
        
        # Validate request body
        blocked_serializer = UserValidateSerializer(data={'username' : blocked})
        blocked_serializer.is_valid(raise_exception=True)

        # Serialize data
        data = {}
        data['prevented'] = prevented_serializer.data
        data['blocked'] = blocked_serializer.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        # Save & Return Block
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        
        # Get request data
        blocked = request.data.get('blocked','')
        
        # Check body
        if not blocked:
            raise BlockedException()
        
        # Validate request body
        blocked_serializer = UserValidateSerializer(data={'username' : blocked})
        blocked_serializer.is_valid(raise_exception=True)
        
        # Delete Block
        try:
            block = Block.objects.get(prevented=request.user.id, blocked=blocked_serializer.data['id'])
            block.delete()
            return Response([])
        except ObjectDoesNotExist:
            raise OperationException()

# User Login Acticity API
class LoginActivityAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = LoginActivitySerializer

    def get(self, request, *args, **kwargs):

        # Serialize activities
        activities = LoginActivity.objects.all()
        serializer = self.get_serializer(activities,many=True)
        
        # Return data
        return Response(serializer.data)