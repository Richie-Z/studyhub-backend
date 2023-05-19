from rest_framework import serializers

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
