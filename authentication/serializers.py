from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid email or password.")
            data["user"] = user
        else:
            raise serializers.ValidationError("Must include 'email' or and 'password'.")

        return data


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "full_name", "confirm_password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        return data

    def create(self, validated_data):
        confirm_password = validated_data.pop("confirm_password", None)
        return User.objects.create_user(**validated_data)
