from django.urls import converters

from authentication.models import User

from .models import Repository


class UserConverter(converters.StringConverter):
    def to_python(self, value):
        try:
            user_id = int(value)
            user = User.objects.get(pk=user_id)
            return user
        except (User.DoesNotExist, ValueError):
            return "is_null"

    def to_url(self, value):
        return str(value.pk)


class RepositoryConverter(converters.StringConverter):
    def to_python(self, value):
        try:
            repository_id = int(value)
            repository = Repository.objects.get(pk=repository_id)
            return repository
        except (Repository.DoesNotExist, ValueError):
            return "is_null"

    def to_url(self, value):
        return str(value.pk)
