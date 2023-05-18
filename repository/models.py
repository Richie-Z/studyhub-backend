from django.db import models
from authentication.models import User


class RepositoryManager(models.Manager):
    def create_repository(self, name, detail, user_id, is_private=False):
        repository = self.model(
            name=name, detail=detail, user_id=user_id, is_private=is_private
        )
        repository.save()
        return repository

    def get_public_repositories(self):
        return self.filter(is_private=False)


class Repository(models.Model):
    name = models.CharField(max_length=255)
    detail = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)

    objects = RepositoryManager()

    def __str__(self):
        return self.name


class StarRepositoryManager(models.Manager):
    def toggle(self, user_id, repository_id):
        try:
            star_repo = self.get(user_id=user_id, repository_id=repository_id)
            star_repo.delete()

            return False  # Indicate that the data was deleted
        except StarRepository.DoesNotExist:
            self.create(user_id=user_id, repository_id=repository_id)

            return True  # Indicate that the data was created


class StarRepository(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    repository_id = models.ForeignKey(Repository, on_delete=models.CASCADE)

    objects = StarRepositoryManager()

    def __str__(self):
        return self.name
