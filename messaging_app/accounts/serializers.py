# Requirements
from rest_framework import serializers
from django.contrib.auth import authenticate, user_logged_in, user_login_failed
from django.core.exceptions import ObjectDoesNotExist

# Models
from django.contrib.auth.models import User
from accounts.models import Block, LoginActivity

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email',)

# User Validation Serializer
class UserValidateSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email',)

    def validate(self,data):
        try:
            user = User.objects.get(username=data['username'])
            return user
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Invalid Username")

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only' : True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'])

        return user

# Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self,data):
        request = self.context.get('request')
        user = authenticate(request=request,**data)
        if user and user.is_active:
            user_logged_in.send(sender=user.__class__, request=request, user=user)
            return user
        raise serializers.ValidationError("Invalid Credentials")

# Block Serializer
class BlockSerializer(serializers.ModelSerializer):
    prevented = UserValidateSerializer()
    blocked = UserValidateSerializer()

    class Meta:
        model = Block
        fields = ('prevented', 'blocked', 'timestamp',)

# Load Block Serializer
class GetBlockSerializer(serializers.ModelSerializer):
    blocked = UserValidateSerializer()

    class Meta:
        model = Block
        fields = ('blocked', 'timestamp',)

# Login Activity Serializer
class LoginActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginActivity
        fields = '__all__'