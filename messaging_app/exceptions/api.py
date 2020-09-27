from rest_framework import generics, permissions
from exceptions.models import ExceptionModel
from exceptions.serializers import ExceptionSerializer
from rest_framework.response import Response

class ExceptionAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = ExceptionSerializer
    
    def get(self, request, *args, **kwargs):
        exceptions = ExceptionModel.objects.all()
        serializer = self.get_serializer(exceptions,many=True)
        return Response(serializer.data)