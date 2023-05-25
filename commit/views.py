from rest_framework import status
from rest_framework.decorators import parser_classes, permission_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from project.helpers import create_response

from .models import Commit
from .serializers import (
    CommitDetailSerializer,
    CommitSerializer,
    FileSerializer,
    FolderSerializer,
    RollbackSerializer,
)


@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
class CreateCommitFile(APIView):
    def post(self, request):
        commit_serializer = CommitSerializer(data=request.data)
        if not commit_serializer.is_valid():
            return create_response(
                "Error Create Commit",
                status.HTTP_400_BAD_REQUEST,
                {"errors": commit_serializer.errors},
            )

        commit_file_serializer = FileSerializer(data=request.data)
        if not commit_file_serializer.is_valid():
            return create_response(
                "Error Create Commit (File)",
                status.HTTP_400_BAD_REQUEST,
                {"errors": commit_file_serializer.errors},
            )
        commit = commit_serializer.save(user=request.user)
        commit_file_serializer.save(commit=commit)
        return create_response("Success Create Commit", status.HTTP_201_CREATED)


@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
class CreateCommitFolder(APIView):
    def post(self, request):
        commit_serializer = CommitSerializer(data=request.data)
        if not commit_serializer.is_valid():
            return create_response(
                "Error Create Commit",
                status.HTTP_400_BAD_REQUEST,
                {"errors": commit_serializer.errors},
            )

        commit_folder_serializer = FolderSerializer(data=request.data)
        if not commit_folder_serializer.is_valid():
            return create_response(
                "Error Create Commit (folder)",
                status.HTTP_400_BAD_REQUEST,
                {"errors": commit_folder_serializer.errors},
            )

        commit_file_serializer = FileSerializer(data=request.data)
        if not commit_file_serializer.is_valid():
            return create_response(
                "Error Create Commit (File)",
                status.HTTP_400_BAD_REQUEST,
                {"errors": commit_file_serializer.errors},
            )
        commit = commit_serializer.save(user=request.user)
        commit_folder = commit_folder_serializer.save(commit=commit)
        commit_file_serializer.save_folder(commit=commit, commit_folder=commit_folder)

        return create_response("Success Create Commit", status.HTTP_201_CREATED)


@permission_classes([IsAuthenticated])
class GetCommitDetail(APIView):
    def get(self, request, *args, **kwargs):
        commit = kwargs.get("commit")
        if commit == "is_null":
            return create_response("Invalid Commit ID", status.HTTP_404_NOT_FOUND)

        try:
            serializer = CommitDetailSerializer(commit, context={"request": request})
            data = serializer.data
            return create_response("Get Data Success", status.HTTP_200_OK, data)
        except Commit.DoesNotExist:
            return create_response("Get Data Success", status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class ActivateCommit(APIView):
    def post(self, request):
        rollback_serializer = RollbackSerializer(data=request.data)
        if not rollback_serializer.is_valid():
            return create_response(
                "Error Activating Commit",
                status.HTTP_400_BAD_REQUEST,
                {"errors": rollback_serializer.errors},
            )

        rollback_serializer.active()
        return create_response("Success Activating Commit", status.HTTP_200_OK)
