from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/authentication/", include("authentication.urls")),
    path("api/repository/", include("repository.urls")),
    path("api/commit/", include("commit.urls")),
]
