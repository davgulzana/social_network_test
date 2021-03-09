from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(min_length=8)
    password_confirmation = serializers.CharField(min_length=8, write_only=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("User with this username already exists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exists")
        return value

    def validate(self, attrs):
        password = attrs.get("password", "")
        password_confirmation = attrs.get("password_confirmation", "")
        if password != password_confirmation:
            raise serializers.ValidationError("Wrong password confirmation")
        attrs.pop("password_confirmation")
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        self.user.last_login = timezone.now()
        self.user.save()
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, validated_data):
        new_password = validated_data.get("new_password")
        new_password_confirm = validated_data.get("new_password_confirm")
        if new_password != new_password_confirm:
            raise serializers.ValidationError("Passwords don't match")
        return validated_data


class ResetPasswordSerializer(serializers.Serializer):
    activation_code = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    def validate_activation_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError("Wrong activation code")
        return code

    def validate(self, validated_data):
        new_password = validated_data.get("new_password")
        new_password_confirm = validated_data.get("new_password_confirm")
        if new_password != new_password_confirm:
            raise serializers.ValidationError("Passwords don't match")
        return validated_data


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)

    class Meta:
        fields = ("username", "email", "first_name", "last_name", "avatar")
        model = User
