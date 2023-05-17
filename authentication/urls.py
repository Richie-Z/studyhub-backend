from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from .views import LoginView, RegisterView, UserInfoView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login", LoginView.as_view(), name="login"),
    path("me", UserInfoView.as_view(), name="me"),
    path("register", RegisterView.as_view(), name="register"),
]
