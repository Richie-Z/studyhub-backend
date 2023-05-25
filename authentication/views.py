from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from project.helpers import create_response

from .models import User
from .serializers import LoginSerializer, RegistrationSerializer


class Login(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        refresh = RefreshToken.for_user(user)

        return create_response(
            "Success Login",
            status.HTTP_200_OK,
            data={
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
        )


@permission_classes([IsAuthenticated])
class GetUserInfo(APIView):
    def get(self, request):
        user = request.user
        data = {
            "user": {"username": user.username, "email": user.email},
        }
        return create_response("Success Get User", status.HTTP_200_OK, data)


class Register(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            return create_response("Success Register", status.HTTP_201_CREATED)
        else:
            return create_response(
                "Error while creating user",
                status.HTTP_400_BAD_REQUEST,
                {"errors": serializer.errors},
            )
