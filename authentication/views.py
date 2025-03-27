from django.shortcuts import render
from rest_framework import generics, status 
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
# Create your views here.

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def index(request):
    data = {
        "message":f"Hello {request.user.username}, welcome to your user area"
    }
    return Response(data)

class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data 
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True) 
        serializer.save() 

        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)