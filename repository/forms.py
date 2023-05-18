from django import forms

from .models import Repository


class RepositoryForm(forms.ModelForm):
    class Meta:
        model = Repository
        fields = ["repository_name", "repository_detail", "user", "is_private"]
