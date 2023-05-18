from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.forms import RegistrationForm
from authentication.models import User
from project.helpers import create_response

from .serializers import LoginSerializer


class LoginView(APIView):
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
class UserInfoView(APIView):
    def get(self, request):
        user = request.user
        data = {
            "user": {"username": user.username, "email": user.email},
        }
        return create_response("Success Get User", status.HTTP_200_OK, data)


class RegisterView(APIView):
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            full_name = form.cleaned_data["full_name"]

            user = User.objects.create_user(
                username=username, full_name=full_name, email=email, password=password
            )
            return create_response("Success Register", status.HTTP_201_CREATED)

        else:
            return create_response(
                "Error while creating user",
                status.HTTP_400_BAD_REQUEST,
                {"errors": form.errors},
            )
