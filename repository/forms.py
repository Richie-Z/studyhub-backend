from django import forms

from .models import Repository, RepositoryStar


class RepositoryForm(forms.ModelForm):
    class Meta:
        model = Repository
        fields = ["repository_name", "repository_detail", "user", "is_private"]


class RepositoryStarForm(forms.ModelForm):
    class Meta:
        model = RepositoryStar
        fields = ["repository"]
