from django.shortcuts import render

from modules.models import Module
from quizzes.models import Quiz


def HomepageView(request):
    modules = Module.objects.all()
    quizzes = Quiz.objects.all()
    ctx = {
        "modules": modules,
        "quizzes": quizzes,
    }
    return render(request, "index.html", ctx)
