from rest_framework import generics, permissions
from exceptions.models import ExceptionModel
from exceptions.serializers import ExceptionSerializer
from rest_framework.response import Response

# Exception API
class ExceptionAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = ExceptionSerializer
    
    def get(self, request, *args, **kwargs):

        # Serialize exception data
        exceptions = ExceptionModel.objects.all()
        serializer = self.get_serializer(exceptions,many=True)
        
        # Return serialized data
        return Response(serializer.data)