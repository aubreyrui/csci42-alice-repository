from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy

from .models import ModuleCategory, Module, Comment, Gallery
from .forms import CommentForm
from accounts.models import Profile

class CategoryListView(ListView):
    model = ModuleCategory
    template_name = ""

def ModuleDetailView(request, pk):
    module = Module.objects.get(pk=pk)
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = Comment()
            comment.author = Profile.objects.get(user=request.user)
            comment.entry = form.cleaned_data.get("entry")
            comment.module = Module.objects.get(pk=pk)
            comment.save()
            return redirect("modules:Module", pk=pk)
        
    ctx = {
        "object": module,
        "form": form,
        "allModules": Module.objects.all(),
        "comments": Comment.objects.all(),
    }
    return render(request, "modules__module.html", ctx)