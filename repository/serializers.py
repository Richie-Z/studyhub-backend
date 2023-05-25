import itertools

from rest_framework import serializers, status
from rest_framework.exceptions import APIException

from commit.models import Commit, CommitFile, CommitFolder
from commit.serializers import SimpleCommitFileSerializer, SimpleCommitFolderSerializer
from project.helpers import create_response

from .models import Repository, RepositoryStar


class SimpleRepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository
        fields = ["repository_name", "repository_detail", "is_private"]


class RepositorySerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()

    class Meta:
        model = Repository
        fields = [
            "id",
            "repository_name",
            "repository_detail",
            "is_private",
            "star_count",
            "is_starred",
        ]

    def get_star_count(self, obj):
        return RepositoryStar.objects.filter(repository=obj).count()

    def get_is_starred(self, obj):
        user = self.context.get("request").user
        if user and user.is_authenticated:
            return RepositoryStar.objects.filter(repository=obj, user=user).exists()
        return False

    def save(self, **kwargs):
        repository_name = self.validated_data.get("repository_name")
        repository_detail = self.validated_data.get("repository_detail")
        user = kwargs.get("user")
        repository = Repository.objects.create_repository(
            repository_name=repository_name,
            repository_detail=repository_detail,
            user=user,
        )

        return repository


def process_folder(data):
    # Create a dictionary to store the unique combinations of folder_name and file_name with their corresponding maximum ids
    unique_entries = {}

    for element in data:
        folder_name = element["folder_name"]
        commit_files = element["commit_file"]
        for file in commit_files:
            filename = file["file_name"]
            file_id = file["id"]
            key = (folder_name, filename)

            if key not in unique_entries or file_id > unique_entries[key]["id"]:
                unique_entries[key] = file

    # Group the unique entries by folder_name
    grouped_data = {}
    for key, file in unique_entries.items():
        folder_name, _ = key
        if folder_name not in grouped_data:
            grouped_data[folder_name] = {
                "id": file["id"],
                "folder_name": folder_name,
                "commit_file": [],
            }
        grouped_data[folder_name]["commit_file"].append(file)

    # Convert the grouped data into a list
    result = list(grouped_data.values())
    return result


def process_file(data):
    unique_files = {}
    for item in data:
        file_name = item["file_name"]
        if file_name not in unique_files or unique_files[file_name]["id"] < item["id"]:
            unique_files[file_name] = item

    return sorted(unique_files.values(), key=lambda x: x["file_name"])


class RepositoryDetailSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()

    class Meta:
        model = Repository
        fields = [
            "id",
            "repository_name",
            "repository_detail",
            "is_private",
            "star_count",
            "data",
        ]

    def get_star_count(self, obj):
        return RepositoryStar.objects.filter(repository=obj).count()

    def get_data(self, obj):
        commits = Commit.objects.filter(repository=obj, is_rollback=False)
        folder_data = []
        file_data = []

        for commit in commits:
            commit_folder = CommitFolder.objects.filter(commit=commit)
            folder_data.append(
                SimpleCommitFolderSerializer(commit_folder, many=True).data
            )

            commit_file = CommitFile.objects.filter(commit=commit, commit_folder=None)
            file_data.append(SimpleCommitFileSerializer(commit_file, many=True).data)
        folder_data = itertools.chain(*folder_data)
        file_data = itertools.chain(*file_data)

        folder_result = process_folder(folder_data)
        file_result = process_file(file_data)

        return {"folder": folder_result, "file": file_result}


class RepositoryCommitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commit
        fields = ["id", "commit_msg", "repository", "commit_date"]


class RepositoryStarSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepositoryStar
        fields = ["user", "repository"]
        extra_kwargs = {"user": {"required": False}}

    def save(self, **kwargs):
        repository = self.validated_data["repository"]
        user = kwargs.get("user")
        repo = RepositoryStar.objects.toggle(user=user, repository=repository)
        return repo


class CommitFolderNotFoundError(APIException):
    status_code = 404
    default_detail = (
        "Commit folder not found for the specified repository and folder name."
    )
    default_code = "commit_folder_not_found"


class FolderFileSerializer(serializers.Serializer):
    folder_name = serializers.CharField()
    files = serializers.SerializerMethodField()

    def get_files(self, obj):
        folder_name = self.validated_data["folder_name"]
        repository = self.context.get("repository")
        commit_folder = CommitFolder.objects.filter(
            folder_name=folder_name, commit__repository=repository
        )

        if not commit_folder.exists():
            raise CommitFolderNotFoundError()

        file_data = []
        for folder in commit_folder:
            file = CommitFile.objects.filter(commit_folder=folder)
            file_data.append(SimpleCommitFileSerializer(file, many=True).data)

        file_data = itertools.chain(*file_data)

        file_result = process_file(file_data)

        return file_result
