from django.urls import path

from repository.views import CreateRepositoryView, RepositoryStarView

urlpatterns = [
    path("", CreateRepositoryView.as_view(), name="create_repo"),
    path("toggle", RepositoryStarView.as_view(), name="toggle_star"),
]
