from django.shortcuts import render
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from authentication.serializers import RegisterSerializer, LoginSerializer, OperationSerializer
from rest_framework import response, status, permissions
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import User

class AuthUserAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        
        return response.Response({'user':serializer.data})



class RegisterAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class= RegisterSerializer
    
    def post(self,request):
        serializers=self.serializer_class(data=request.data)
        
        if serializers.is_valid():
            serializers.save()

            return response.Response(serializers.data,status=status.HTTP_201_CREATED)
        
        return response.Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)
    
class LoginAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class= LoginSerializer
    
    def post(self,request):
        email = request.data.get('email',None)
        password = request.data.get('password',None)
        
        user=authenticate(username=email, password=password)
        
        if user:
            serializer = self.serializer_class(user)
            
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response({'message':"Invalid Credentials, Try Again"},status=status.HTTP_200_OK)
    

class OperationAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = []    
    queryset = User.objects.all()
    serializer_class = OperationSerializer
    lookup_field = "id"

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.kwargs.get("id"))
        self.check_object_permissions(self.request, obj)
        return obj