from django.urls import converters

from authentication.models import User

from .models import Commit


class CommitConverter(converters.StringConverter):
    def to_python(self, value):
        try:
            commit_id = int(value)
            commit = Commit.objects.get(pk=commit_id)
            return commit
        except (Commit.DoesNotExist, ValueError):
            return "is_null"

    def to_url(self, value):
        return str(value.pk)
