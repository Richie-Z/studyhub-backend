from rest_framework import serializers

from .models import Commit, CommitFile, CommitFolder


class CommitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commit
        fields = ["id", "commit_msg", "repository"]

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
        fields = ["upload_path", "commit_folder"]

    def save(self, **kwargs):
        upload_paths = self.validated_data.pop("upload_path", [])
        commit_folder = self.validated_data.get("commit_folder")
        commit = kwargs.get("commit")
        if commit_folder is not None:
            new_commit_folder = CommitFolder.objects.create_folder(
                commit=commit, folder_name=str(commit_folder)
            )
            for upload_path in upload_paths:
                CommitFile.objects.create_file(
                    commit=commit,
                    upload_path=upload_path,
                    commit_folder=new_commit_folder,
                )

        else:
            for upload_path in upload_paths:
                CommitFile.objects.create_file(
                    commit=commit,
                    upload_path=upload_path,
                )

    def save_folder(self, **kwargs):
        upload_paths = self.validated_data.pop("upload_path", [])
        commit_folder = kwargs.get("commit_folder")
        commit = kwargs.get("commit")
        for upload_path in upload_paths:
            CommitFile.objects.create_file(
                commit=commit, upload_path=upload_path, commit_folder=commit_folder
            )


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommitFolder
        fields = ["folder_name"]

    def save(self, **kwargs):
        folder_name = self.validated_data["folder_name"]
        commit = kwargs.get("commit")
        folder = CommitFolder.objects.create_folder(
            commit=commit, folder_name=folder_name
        )
        return folder


class SimpleCommitFileSerializer(serializers.ModelSerializer):
    file_name = serializers.SerializerMethodField()

    class Meta:
        model = CommitFile
        fields = ["id", "upload_path", "file_name"]

    def get_file_name(self, obj):
        return str(obj)


class SimpleCommitFolderSerializer(serializers.ModelSerializer):
    commit_file = SimpleCommitFileSerializer(many=True, source="commitfile_set")

    class Meta:
        model = CommitFolder
        fields = ["folder_name", "commit_file"]


class CommitDetailSerializer(serializers.ModelSerializer):
    folder_or_file = serializers.SerializerMethodField()

    class Meta:
        model = Commit
        fields = ["commit_msg", "folder_or_file"]

    def get_folder_or_file(self, obj):
        commit_folders = CommitFolder.objects.filter(commit=obj)
        if commit_folders.exists():
            serializer = SimpleCommitFolderSerializer(commit_folders, many=True)
        else:
            commit_file = CommitFile.objects.filter(commit=obj)
            serializer = SimpleCommitFileSerializer(commit_file, many=True)

        return serializer.data


class RollbackSerializer(serializers.Serializer):
    commit = serializers.PrimaryKeyRelatedField(queryset=Commit.objects.all())

    def active(self):
        try:
            Commit.objects.filter(is_active=True).update(is_active=False)

            commit_instance = self.validated_data["commit"]
            commit_instance.is_active = True
            commit_instance.is_rollback = False
            commit_instance.save()

            prev_commits = Commit.objects.filter(id__lt=commit_instance.id)
            prev_commits.update(is_rollback=False)

            next_commits = Commit.objects.filter(id__gt=commit_instance.id)
            next_commits.update(is_rollback=True)

            return True
        except Commit.DoesNotExist:
            return False
