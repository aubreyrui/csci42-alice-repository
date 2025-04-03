from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from accounts.models import Profile


class ProfileCreationForm(UserCreationForm):
    email = forms.EmailField()
    display_name = forms.CharField(max_length=63)

    class Meta:
        model = User
        fields = ["username", "display_name", "email", "password1", "password2"]

    template_name = "profile_create_snippet.html"
