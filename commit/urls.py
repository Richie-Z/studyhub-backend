from django.urls import path, register_converter

from commit.converters import CommitConverter
from commit.views import CreateCommitFile, CreateCommitFolder, GetCommitDetail

register_converter(CommitConverter, "commit")
urlpatterns = [
    path("file", CreateCommitFile.as_view(), name="create_commit"),
    path("folder", CreateCommitFolder.as_view(), name="create_commit_folder"),
    path(
        "detail/<commit:commit>",
        GetCommitDetail.as_view(),
        name="detail_commit",
    ),
]
