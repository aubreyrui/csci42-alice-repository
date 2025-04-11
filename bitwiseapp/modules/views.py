from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from django.http import HttpResponse
import traceback
from io import StringIO
from contextlib import redirect_stdout

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

class ModuleUpdateView(UpdateView):
    model = Module
    fields = ["title", "category", "entry",]
    template_name = "modules/modules_modUpdate.html"

    def get_success_url(self):
        return reverse_lazy("modules:Module",
            kwargs={
                "pk": self.object.pk
            })
    
class GalleryCreateView(LoginRequiredMixin, CreateView):
    model = Gallery
    template_name = "modules/modules_addGallery.html"
    def get_success_url(self):
        return reverse_lazy("modules:Module",
            kwargs={
                "pk": self.object.module.pk
            })
    
# COMPILER STUFF BELOW THIS POINT

def Execute(code): 
    try:
        # Capture standard output in a buffer
        output_buffer = StringIO()
        with redirect_stdout(output_buffer):
            exec(code)
        output = output_buffer.getvalue()
    except Exception as e:
        # Provide detailed error information
        output = f"Error: {str(e)}\n{traceback.format_exc()}"
    return output

def Compiler(request):
    return render(request, "modules/modules_code.html")

def Compile(request): 
    if request.method == "POST":
        codeareadata = request.POST['codearea']
        output = Execute(codeareadata)
        return render(request, "modules/modules_code.html", {"code": codeareadata, "output": output})
    return HttpResponse("Method not allowed", status=405)