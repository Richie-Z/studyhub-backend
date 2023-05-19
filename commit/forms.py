from django import forms

from .models import Commit, CommitFile, CommitFolder


class CommitForm(forms.ModelForm):
    class Meta:
        model = Commit
        fields = ["commit_msg", "repository"]


class FolderForm(forms.ModelForm):
    class Meta:
        model = CommitFolder
        fields = ["folder_name"]


class FileForm(forms.ModelForm):
    class Meta:
        model = CommitFile
        fields = ["file_name"]
