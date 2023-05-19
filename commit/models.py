import datetime

from django.db import models

from authentication.models import User
from repository.models import Repository


class CommitManager(models.Manager):
    def create_commit(
        self,
        commit_msg,
        user,
        repository,
        commit_date,
        is_active=True,
        is_rollback=False,
    ):
        self.filter(is_active=True).update(is_active=False)

        commit = self.model(
            commit_msg=commit_msg,
            user=user,
            repository=repository,
            commit_date=datetime.date.today(),
            is_active=is_active,
            is_rollback=is_rollback,
        )
        commit.save()
        return commit


class Commit(models.Model):
    class Meta:
        db_table = "commit"

    commit_msg = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    commit_date = models.DateField()
    is_active = models.BooleanField(default=True)
    is_rollback = models.BooleanField(default=False)

    objects = CommitManager()

    def __str__(self) -> str:
        return self.commit_msg


class FolderManager(models.Manager):
    def create_folder(self, commit, folder_name):
        folder = self.model(commit=commit, folder_name=folder_name)
        folder.save()
        return folder


class CommitFolder(models.Model):
    class Meta:
        db_table = "commit_folder"

    commit = models.ForeignKey(Commit, on_delete=models.CASCADE)
    folder_name = models.CharField(max_length=255)

    objects = FolderManager()

    def __str__(self) -> str:
        return self.folder_name


class FileManager(models.Manager):
    def create_file(self, commit, file_name, commit_folder_id):
        file = self.model(
            commit=commit, file_name=file_name, commit_folder_id=commit_folder_id
        )
        file.save()
        return file


class CommitFile(models.Model):
    class Meta:
        db_table = "commit_file"

    commit = models.ForeignKey(Commit, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    commit_folder_id = models.ForeignKey(
        CommitFolder, on_delete=models.CASCADE, null=True
    )

    objects = FileManager()

    def __str__(self) -> str:
        return self.file_name
