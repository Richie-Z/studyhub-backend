from django.urls import path

from commit.views import CreateCommitFileView

urlpatterns = [path("file", CreateCommitFileView.as_view(), name="create_commit")]
