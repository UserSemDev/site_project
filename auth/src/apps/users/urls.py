from django.urls import path

from apps.users.apps import UsersConfig
from apps.users.views import SigninView, SignupView, TokenVerificationView

app_name = UsersConfig.name

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("signin/", SigninView.as_view(), name="signin"),
    path("webhook/verify/", TokenVerificationView.as_view(), name="webhook-verify"),
]
