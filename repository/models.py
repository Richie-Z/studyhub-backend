from django.db import models
from django.utils.text import slugify

from authentication.models import User


class RepositoryManager(models.Manager):
    def create_repository(
        self, repository_name, repository_detail, user, is_private=False
    ):
        repository = self.model(
            repository_name=slugify(repository_name),
            repository_detail=repository_detail,
            user=user,
            is_private=is_private,
        )
        repository.save()
        return repository

    def get_public_repositories(self):
        return self.filter(is_private=False)


class Repository(models.Model):
    class Meta:
        db_table = "repository"

    repository_name = models.CharField(max_length=255)
    repository_detail = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)

    objects = RepositoryManager()

    def __str__(self):
        return self.name


class RepositoryStarManager(models.Manager):
    def toggle(self, user, repository):
        try:
            star_repo = self.get(user=user, repository=repository)
            star_repo.delete()

            return False  # Indicate that the data was deleted
        except RepositoryStar.DoesNotExist:
            self.create(user=user, repository=repository)

            return True  # Indicate that the data was created


class RepositoryStar(models.Model):
    class Meta:
        db_table = "repository_star"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)

    objects = RepositoryStarManager()

    def __str__(self):
        return self.name
