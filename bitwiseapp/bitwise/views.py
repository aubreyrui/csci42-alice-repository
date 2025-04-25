from django.shortcuts import render

from modules.models import Module


def HomepageView(request):
    modules = Module.objects.all()
    ctx = {"modules": modules}
    return render(request, "index.html", ctx)
