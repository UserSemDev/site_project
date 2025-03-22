import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from apps.users.models import User
from apps.users.serializers import UserSerializer
from apps.users.utils import generate_jwt, validate_jwt


class SignUpView(APIView):
    @csrf_exempt
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        required_fields = ["username", "email", "password"]
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return JsonResponse(
                {"error": f"Missing fields: {', '.join(missing_fields)}"}, status=400
            )

        if User.objects(username=data["username"]).first():
            return JsonResponse({"error": "Username already exists"}, status=400)

        if User.objects(email=data["email"]).first():
            return JsonResponse({"error": "Email already exists"}, status=400)

        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            token = generate_jwt(user.id)
            return JsonResponse({"jwt": token}, status=201)
        return JsonResponse({"error": serializer.errors}, status=400)


class SignInView(APIView):
    @csrf_exempt
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return JsonResponse(
                {"error": "Missing fields: username, password"}, status=400
            )

        user = User.objects(username=username).first()
        if not user or not user.check_password(password):
            return JsonResponse({"error": "Invalid username or password"}, status=401)

        user.update_last_login()
        token = generate_jwt(user.id)
        return JsonResponse({"jwt": token}, status=200)


class AuthView(APIView):
    def get(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JsonResponse({"error": "Missing authorization header"}, status=403)

        token = auth_header.split(" ")[1]
        payload = validate_jwt(token)
        if payload:
            user_id = payload["user_id"]
            user = User.objects(id=user_id).first()
            return JsonResponse(
                {"user": {"username": user.username, "role": user.role}}, status=200
            )
        return JsonResponse({"error": "Invalid token"}, status=401)
