from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from accounts.models import Profile


class ProfileCreationForm(UserCreationForm):
    email = forms.EmailField()
    display_name = forms.CharField(max_length=63)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "display_name",
                  "email", "password1", "password2"]
