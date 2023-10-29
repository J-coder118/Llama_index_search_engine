from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.serializers import Serializer, FileField
from django.http import JsonResponse

User = get_user_model()

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    def validate(self, attrs):
        # Perform any additional validation or authentication logic here
        # For example, you can authenticate the user using Django's authenticate() method
        # and raise a validation error if authentication fails
        username = attrs.get('username')
        password = attrs.get('password')

        print(username, password)
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('Invalid username or password.')
        return attrs

class UserSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    password = serializers.CharField(min_length=8, max_length=32, write_only=True)
    email = serializers.EmailField(max_length=50, allow_blank=False)
    
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        print("dddddd")
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        print("username", username)
        print("user", username, email, password)
        user_obj = User(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()

        response_json = {
            "status": "success",
            "data": user_obj
        }

        print("response data", response_json)
        # return JsonResponse(response_json)JsonResponse
        # return "dsfdsf"
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'file', 'uploaded_at')