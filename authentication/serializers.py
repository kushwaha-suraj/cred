from rest_framework import serializers
from .models import User,MyUserManager

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    
    class Meta:
        model = User
        fields = ['id','username', 'email', 'password']
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    
    class Meta:
        model = User
        fields = [ 'id','email','username', 'password', 'token']
        
        read_only_fields = ['token']
        
        
class OperationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    
    class Meta:
        model = User
        fields = [ 'id', 'email','username', 'password', 'token']
        
        read_only_fields = ['token']
        

