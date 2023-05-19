# Create your views here.
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from project.helpers import create_response
from repository.models import Repository, RepositoryStar
from repository.serializers import RepositorySerializer

from .forms import CommitForm


@permission_classes([IsAuthenticated])
class CreateCommitFileView(APIView):
    def post(self, request):
        commit_form = CommitForm(request.POST)
        if commit_form.is_valid():
            repository_name = commit_form.cleaned_data["repository_name"]
            repository_detail = commit_form.cleaned_data["repository_detail"]
            user = commit_form.cleaned_data["user"]
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
