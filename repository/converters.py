from django.urls import converters

from authentication.models import User


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
