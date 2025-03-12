import datetime

import bcrypt
import pytz
from rest_framework import serializers

from core import settings


class UserSerializer(serializers.Serializer):
    """Сериализатор пользователя"""
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    role = serializers.ChoiceField(choices=["user", "admin"], default="user")
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Проверяем, есть ли уже пользователь с таким email или username"""
        from core.settings import MONGO_USERS_COLLECTION

        if MONGO_USERS_COLLECTION.find_one({"username": data["username"]}):
            raise serializers.ValidationError("Username already exists")

        if MONGO_USERS_COLLECTION.find_one({"email": data["email"]}):
            raise serializers.ValidationError("Email already exists")

        return data

    def set_password(self, raw_password):
        """Хэширование пароля с использованием bcrypt и случайной соли"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(raw_password.encode("utf-8"), salt).decode("utf-8")

    def create(self, validated_data):
        """Сохраняем пользователя в MongoDB"""
        from core.settings import MONGO_USERS_COLLECTION

        tz = pytz.timezone(settings.TIME_ZONE)
        current_time = datetime.datetime.now(tz)

        user_data = {
            "username": validated_data["username"],
            "email": validated_data["email"],
            "role": validated_data.get("role", "user"),
            "password": self.set_password(validated_data["password"]),
            "data_joined": current_time,
            "last_login": None,
        }
        MONGO_USERS_COLLECTION.insert_one(user_data)
        return user_data
