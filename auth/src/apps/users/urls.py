from django.urls import path

from apps.users.apps import UsersConfig
from apps.users.views import AuthView, SignInView, SignUpView

app_name = UsersConfig.name

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signin/", SignInView.as_view(), name="signin"),
    path("auth/", AuthView.as_view(), name="auth"),
]
