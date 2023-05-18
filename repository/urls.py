from django.urls import path

from repository.views import CreateRepositoryView

urlpatterns = [path("", CreateRepositoryView.as_view(), name="create_repo")]
