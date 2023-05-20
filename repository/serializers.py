from rest_framework import serializers

from authentication.models import User

from .models import Repository, RepositoryStar


class RepositorySerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()

    class Meta:
        model = Repository
        fields = [
            "repository_name",
            "repository_detail",
            "is_private",
            "star_count",
            "is_starred",
        ]

    def get_star_count(self, obj):
        return RepositoryStar.objects.filter(repository=obj).count()

    def get_is_starred(self, obj):
        user = self.context.get("request").user
        if user and user.is_authenticated:
            return RepositoryStar.objects.filter(repository=obj, user=user).exists()
        return False

    def save(self, **kwargs):
        repository_name = self.validated_data.get("repository_name")
        repository_detail = self.validated_data.get("repository_detail")
        user = kwargs.get("user")
        repository = Repository.objects.create_repository(
            repository_name=repository_name,
            repository_detail=repository_detail,
            user=user,
        )

        return repository


class RepositoryStarSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepositoryStar
        fields = ["user", "repository"]
        extra_kwargs = {"user": {"required": False}}

    def save(self, **kwargs):
        repository = self.validated_data["repository"]
        user = kwargs.get("user")
        repo = RepositoryStar.objects.toggle(user=user, repository=repository)
        return repo
