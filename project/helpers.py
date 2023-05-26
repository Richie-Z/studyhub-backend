from functools import wraps

from rest_framework import status
from rest_framework.response import Response

from repository.models import Repository


def create_response(message, status_code, data=None):
    return Response(
        data={"status_code": status_code, "message": message, "data": data},
        status=status_code,
    )


def user_repo_checker(view_func):
    @wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        repository = kwargs.get("repository") or Repository.objects.get(
            id=request.data.get("repository")
        )
        user = request.user

        if (
            isinstance(repository, Repository)
            and repository.user != user
            and repository.is_private
        ):
            return create_response(
                "You don't have access to Enter", status.HTTP_401_UNAUTHORIZED
            )

        return view_func(self, request, *args, **kwargs)

    return wrapper
