from django.urls import path, register_converter

from repository.views import (
    CreateRepository,
    GetAllRepository,
    GetRepositoryComitList,
    GetRepositoryDetail,
    ToggleRepositoryStar,
)

from .converters import RepositoryConverter, UserConverter

register_converter(UserConverter, "user")
register_converter(RepositoryConverter, "repository")

urlpatterns = [
    path("", CreateRepository.as_view(), name="create_repo"),
    path("toggle", ToggleRepositoryStar.as_view(), name="toggle_star"),
    path("all", GetAllRepository.as_view(), name="get_all"),
    path("all/<user:user>", GetAllRepository.as_view(), name="get_all"),
    path(
        "detail/<repository:repository>",
        GetRepositoryDetail.as_view(),
        name="get_repo_detail",
    ),
    path(
        "repository/<repository:repository>",
        GetRepositoryComitList.as_view(),
        name="get_repo_commit",
    ),
]
