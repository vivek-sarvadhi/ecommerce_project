from rest_framework import serializers
from users.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    user_type = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email','user_type']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    # user_type = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email']