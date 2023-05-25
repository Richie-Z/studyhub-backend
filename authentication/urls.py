from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import GetUserInfo, Login, Register

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login", Login.as_view(), name="login"),
    path("me", GetUserInfo.as_view(), name="me"),
    path("register", Register.as_view(), name="register"),
]
