from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.Serializer):
    """Сериализатор пользователя"""

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=["user", "admin"], default="user")
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        """Создание пользователя с хешированием пароля"""
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            role=validated_data.get("role", "user")
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
