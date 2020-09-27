from rest_framework import serializers
from exceptions.models import ExceptionModel
from django.contrib.auth.models import User

class ExceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExceptionModel
        fields = '__all__'