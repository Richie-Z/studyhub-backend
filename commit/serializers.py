import django.urls
from rest_framework import serializers

from .models import Commit, CommitFile


class CommitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commit
        fields = ["commit_msg", "repository"]

    def save(self, **kwargs):
        commit_msg = self.validated_data["commit_msg"]
        repository = self.validated_data["repository"]
        user = kwargs.get("user")
        commit = Commit.objects.create_commit(
            commit_msg=commit_msg, repository=repository, user=user
        )
        return commit


class FileSerializer(serializers.ModelSerializer):
    upload_path = serializers.ListField(
        child=serializers.FileField(), allow_empty=False
    )

    class Meta:
        model = CommitFile
        fields = ["upload_path"]

    def save(self, **kwargs):
        upload_paths = self.validated_data.pop("upload_path", [])
        commit = kwargs.get("commit")
        for upload_path in upload_paths:
            CommitFile.objects.create_file(commit=commit, upload_path=upload_path)
