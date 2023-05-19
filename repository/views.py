from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from project.helpers import create_response
from repository.models import Repository, RepositoryStar
from repository.serializers import RepositorySerializer

from .forms import RepositoryForm, RepositoryStarForm


@permission_classes([IsAuthenticated])
class CreateRepositoryView(APIView):
    def post(self, request):
        form = RepositoryForm(request.POST)
        if form.is_valid():
            repository_name = form.cleaned_data["repository_name"]
            repository_detail = form.cleaned_data["repository_detail"]
            user = form.cleaned_data["user"]
            repository = Repository.objects.create_repository(
                repository_name=repository_name,
                repository_detail=repository_detail,
                user=user,
            )
            return create_response("Success Create Repository", status.HTTP_201_CREATED)
        else:
            return create_response(
                "Error Create Repository",
                status.HTTP_400_BAD_REQUEST,
                {"errors": form.errors},
            )


@permission_classes([IsAuthenticated])
class RepositoryStarView(APIView):
    def post(self, request):
        user = request.user
        form = RepositoryStarForm(request.POST)
        if form.is_valid():
            repository = form.cleaned_data["repository"]
            RepositoryStar.objects.toggle(user=user, repository=repository)
            return create_response("Success Toggle star Repository", status.HTTP_200_OK)
        else:
            return create_response(
                "Error Toggle Repository",
                status.HTTP_400_BAD_REQUEST,
                {"errors": form.errors},
            )


@permission_classes([IsAuthenticated])
class GetAllRepository(APIView):
    def get(self, request, *args, **kwargs):
        user = self.kwargs.get("user") or request.user
        if user == "is_null":
            return create_response("Invalid User ID", status.HTTP_404_NOT_FOUND)
        repository = Repository.objects.get(user=user)
        serializer = RepositorySerializer(repository, context={"request": request})
        data = serializer.data
        return create_response("Get Data Success", status.HTTP_200_OK, data)
