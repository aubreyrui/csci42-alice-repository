from django.urls import path

from .views import CategoryListView, ModuleDetailView, ModuleCreateView, ModuleUpdateView, Execute, Compiler, Compile


urlpatterns = [
    path("list/", CategoryListView.as_view(), name="ModuleCategory"),
    path("lesson/<int:pk>", ModuleDetailView, name="Module"),
    path("lesson/add", ModuleCreateView, name="ModuleCreate"),
    path("lesson/<int:pk>/edit", ModuleUpdateView.as_view(), name="ModuleUpdate"),
    path("compiler", Compiler, name="Compiler"), 
    path("compiler/run", Compile, name="RunCode")
]

app_name = "modules"