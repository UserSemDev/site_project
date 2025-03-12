import datetime
from types import SimpleNamespace

import bcrypt
import pytz
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from apps.users.serializers import UserSerializer
from core.settings import MONGO_USERS_COLLECTION


class SignupView(APIView):
    """Эндпоинт для регистрации"""

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            user_id = user["_id"]
            user_obj = SimpleNamespace(id=user_id)

            refresh = RefreshToken.for_user(user_obj)
            access_token = str(refresh.access_token)
            return Response(
                {
                    "message": "User registered successfully",
                    "user": {"username": user["username"], "role": user["role"]},
                    "access_token": access_token,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)


class SigninView(APIView):
    """Эндпоинт для входа"""

    def check_password(self, raw_password, hashed_password):
        """Проверка пароля через bcrypt"""
        return bcrypt.checkpw(
            raw_password.encode("utf-8"), hashed_password.encode("utf-8")
        )

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        missing_fields = []
        if not username:
            missing_fields.append("username")
        if not password:
            missing_fields.append("password")

        if missing_fields:
            return Response(
                {"error": "Fill in all fields", "missing_fields": missing_fields},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = MONGO_USERS_COLLECTION.find_one({"username": username})
        if user and self.check_password(password, user["password"]):
            tz = pytz.timezone(settings.TIME_ZONE)
            MONGO_USERS_COLLECTION.update_one(
                {"username": username},
                {"$set": {"last_login": datetime.datetime.now(tz)}},
            )

            user_id = user["_id"]
            user_obj = SimpleNamespace(id=user_id)

            refresh = RefreshToken.for_user(user_obj)
            access_token = str(refresh.access_token)

            return Response(
                {
                    "message": "User authenticated successfully",
                    "user": {"username": user["username"], "role": user["role"]},
                    "access_token": access_token,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Incorrect credentials!"}, status=status.HTTP_403_FORBIDDEN
        )


class TokenVerificationView(APIView):
    """Эндпоинт для проверки JWT-токена"""

    def post(self, request):
        token = request.data.get("token")

        if not token:
            return Response(
                {"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            decoded_token = AccessToken(token)
            user_id = decoded_token["user_id"]

            return Response(
                {"message": "Token is valid", "user_id": user_id},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
