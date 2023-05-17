from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator


class RegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        validators=[UnicodeUsernameValidator()],
        help_text="Enter a username",
    )
    email = forms.EmailField(
        validators=[EmailValidator()],
        help_text="Enter your email address",
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        help_text="Enter a password",
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        help_text="Confirm your password",
    )
    full_name = forms.CharField(
        max_length=255,
        help_text="Enter your full name",
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
