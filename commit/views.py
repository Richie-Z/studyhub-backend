from rest_framework import status
from rest_framework.decorators import parser_classes, permission_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from commit.serializers import CommitSerializer, FileSerializer
from project.helpers import create_response


@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
class CreateCommitFileView(APIView):
    def post(self, request):
        commit_serializer = CommitSerializer(data=request.data)
        if not commit_serializer.is_valid():
            return create_response(
                "Error Create Commit",
                status.HTTP_400_BAD_REQUEST,
                {"errors": commit_serializer.errors},
            )

        commit = commit_serializer.save(user=request.user)

        commit_file_serializer = FileSerializer(
            data=request.data, context={"commit": commit}
        )
        if not commit_file_serializer.is_valid():
            return create_response(
                "Error Create Commit (File)",
                status.HTTP_400_BAD_REQUEST,
                {"errors": commit_file_serializer.errors},
            )
        commit_file_serializer.save(commit=commit)
        return create_response("Success Create Commit", status.HTTP_201_CREATED)
