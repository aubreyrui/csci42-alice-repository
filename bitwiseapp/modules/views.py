from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy

from .models import ModuleCategory, Module, Comment, Gallery
from .forms import ModuleForm, CommentForm, GalleryForm
from accounts.models import Profile

class CategoryListView(ListView):
    model = ModuleCategory
    template_name = "modules/modules_list.html"

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

    return render(request, "modules/modules_module.html", ctx)

@login_required
def ModuleCreateView(request):
    form = ModuleForm()

    if request.user.profile.authorized:
        if request.method == "POST":
            form = ModuleForm(request.POST, request.FILES)
            if form.is_valid():
                module = Module()
                module.title = form.cleaned_data.get("title")
                module.category = form.cleaned_data.get("category")
                module.author = Profile.objects.get(user=request.user)
                module.entry = form.cleaned_data.get("entry")
                module.save()
                return redirect("modules:Module", pk=module.pk)

        ctx = {"form": form}
        return render(request, "modules/modules_modCreate.html", ctx)
    else:
        return redirect("bitwise:Index")

class ModuleUpdateView(UpdateView):
    model = Module
    fields = ["title", "category", "entry",]
    template_name = "modules/modules_modUpdate.html"

    def get_success_url(self):
        return reverse_lazy("modules:Module",
            kwargs={
                "pk": self.object.module.pk
            })
    
class GalleryCreateView(LoginRequiredMixin, CreateView):
    model = Gallery
    template_name = "modules/modules_addGallery.html"
    def get_success_url(self):
        return reverse_lazy("modules:Module",
            kwargs={
                "pk": self.object.module.pk
            })