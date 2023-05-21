from django.urls import path, register_converter

from repository.views import (
    CreateRepositoryView,
    GetAllRepository,
    GetRepositoryComitListView,
    RepositoryStarView,
)

from .converters import RepositoryConverter, UserConverter

register_converter(UserConverter, "user")
register_converter(RepositoryConverter, "repository")

urlpatterns = [
    path("", CreateRepositoryView.as_view(), name="create_repo"),
    path("toggle", RepositoryStarView.as_view(), name="toggle_star"),
    path("all", GetAllRepository.as_view(), name="get_all"),
    path("all/<user:user>", GetAllRepository.as_view(), name="get_all"),
    path(
        "repository/<repository:repository>",
        GetRepositoryComitListView.as_view(),
        name="get_repo_commit",
    ),
]
