from accounts.forms import ProfileCreationForm
from django import dispatch
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .models import Profile


class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ["display_name", "email"]
    template_name = "profile_update.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk == self.get_object().pk:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/")

class ProfileCreateView(CreateView):
    model = User
    form_class = ProfileCreationForm
    template_name = "profile_create.html"

    form = ProfileCreationForm()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/")

    def post(self, request, *args, **kwargs):
        form = ProfileCreationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                form.cleaned_data.get("username"),
                form.cleaned_data.get("email"),
                form.cleaned_data.get("password1"),
            )
            user.save()
            profile = Profile()
            profile.user = user
            profile.display_name = form.cleaned_data.get("display_name")
            profile.email = form.cleaned_data.get("email")
            profile.save()
            return HttpResponseRedirect("/registration/login/")
        else:
            return HttpResponseRedirect("/profile/create")
