from django.db import models
from authentication.models import User
from repository.models import Repository


class CommitManager(models.Manager):
    def create_commit(
        self,
        commit_msg,
        user_id,
        repository_id,
        commit_date,
        is_active=True,
        is_rollback=False,
    ):
        self.filter(is_active=True).update(is_active=False)

        commit = self.model(
            commit_msg=commit_msg,
            user_id=user_id,
            repository_id=repository_id,
            commit_date=commit_date,
            is_active=is_active,
            is_rollback=is_rollback,
        )
        commit.save()
        return commit


class Commit(models.Model):
    commit_msg = models.CharField(max_length=255)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    repository_id = models.ForeignKey(Repository, on_delete=models.CASCADE)
    commit_date = models.DateField()
    is_active = models.BooleanField(default=True)
    is_rollback = models.BooleanField(default=False)

    objects = CommitManager()

    def __str__(self) -> str:
        return self.commit_msg


class FolderManager(models.Manager):
    def create_folder(self, commit_id, folder_name):
        folder = self.model(commit_id=commit_id, folder_name=folder_name)
        folder.save()
        return folder


class CommitFolder(models.Model):
    commit_id = models.ForeignKey(Commit, on_delete=models.CASCADE)
    folder_name = models.CharField(max_length=255)

    objects = FolderManager()

    def __str__(self) -> str:
        return self.folder_name


class FileManager(models.Manager):
    def create_file(self, commit_id, file_name, commit_folder_id):
        file = self.model(
            commit_id=commit_id, file_name=file_name, commit_folder_id=commit_folder_id
        )
        file.save()
        return file


class CommitFile(models.Model):
    commit_id = models.ForeignKey(Commit, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    commit_folder_id = models.ForeignKey(
        CommitFolder, on_delete=models.CASCADE, null=True
    )

    objects = FileManager()

    def __str__(self) -> str:
        return self.file_name
