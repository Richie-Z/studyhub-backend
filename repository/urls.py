from django.urls import path, register_converter

from repository.views import CreateRepositoryView, GetAllRepository, RepositoryStarView

from .converters import UserConverter

register_converter(UserConverter, "user")

urlpatterns = [
    path("", CreateRepositoryView.as_view(), name="create_repo"),
    path("toggle", RepositoryStarView.as_view(), name="toggle_star"),
    path("all", GetAllRepository.as_view(), name="get_all"),
    path("all/<user:user>", GetAllRepository.as_view(), name="get_all"),
]
