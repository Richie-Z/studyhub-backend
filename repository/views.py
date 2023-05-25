from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from commit.models import Commit
from project.helpers import create_response
from repository.models import Repository, RepositoryStar
from repository.serializers import (
    RepositoryCommitListSerializer,
    RepositoryDetailSerializer,
    RepositorySerializer,
    RepositoryStarSerializer,
)


@permission_classes([IsAuthenticated])
class CreateRepository(APIView):
    def post(self, request):
        serializer = RepositorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return create_response("Success Create Repository", status.HTTP_201_CREATED)
        else:
            return create_response(
                "Error Create Repository",
                status.HTTP_400_BAD_REQUEST,
                {"errors": serializer.errors},
            )


@permission_classes([IsAuthenticated])
class ToggleRepositoryStar(APIView):
    def post(self, request):
        serializer = RepositoryStarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return create_response("Success Toggle star Repository", status.HTTP_200_OK)
        else:
            return create_response(
                "Error Toggle Repository",
                status.HTTP_400_BAD_REQUEST,
                {"errors": serializer.errors},
            )


@permission_classes([IsAuthenticated])
class GetAllRepository(APIView):
    def get(self, request, *args, **kwargs):
        user = kwargs.get("user") or request.user
        if user == "is_null":
            return create_response("Invalid User ID", status.HTTP_404_NOT_FOUND)
        try:
            repository = Repository.objects.filter(user=user)
            serializer = RepositorySerializer(
                repository, many=True, context={"request": request}
            )
            data = serializer.data
            return create_response("Get Data Success", status.HTTP_200_OK, data)
        except Repository.DoesNotExist:
            return create_response("Get Data Success", status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class GetRepositoryComitList(APIView):
    def get(self, request, *args, **kwargs):
        repo = kwargs.get("repository")
        if repo == "is_null":
            return create_response("Invalid Repository ID", status.HTTP_404_NOT_FOUND)

        try:
            commit = Commit.objects.filter(repository=repo)
            serializer = RepositoryCommitListSerializer(
                commit, many=True, context={"request": request}
            )
            data = serializer.data
            return create_response("Get Data Success", status.HTTP_200_OK, data)
        except Repository.DoesNotExist:
            return create_response("Get Data Success", status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class GetRepositoryDetail(APIView):
    def get(self, request, *args, **kwargs):
        repo = kwargs.get("repository")
        if repo == "is_null":
            return create_response("Invalid Repository ID", status.HTTP_404_NOT_FOUND)

        repository = RepositoryDetailSerializer(repo)
        data = repository.data
        return create_response("Get Data Success", status.HTTP_200_OK, data)
