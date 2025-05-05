from django.urls import path

from .views import (
    CategoryListView,
    CommentDeleteView,
    PythonCompile,
    PythonCompiler,
    WebCompiler, 
    Execute,
    CodeRedirect, 
    GalleryDeleteView,
    ModuleCreateView,
    SearchResultsView,
    ModuleDeleteView,
    ModuleDetailView,
    ModuleUpdateView,
)

urlpatterns = [
    path("list/", CategoryListView.as_view(), name="ModuleCategory"),
    path("lesson/<int:pk>", ModuleDetailView, name="Module"),
    path("lesson/add", ModuleCreateView, name="ModuleCreate"),
    path("search/", SearchResultsView, name="ModuleSearch"),
    path("lesson/<int:pk>/edit", ModuleUpdateView.as_view(), name="ModuleUpdate"),
    path("lesson/<int:pk>/delete", ModuleDeleteView, name="ModuleDelete"),
    path("lesson/<int:pk>/comment/delete", CommentDeleteView, name="CommentDelete"),
    path("lesson/<int:pk>/gallery/delete", GalleryDeleteView, name="GalleryDelete"),
    path("code/python", PythonCompiler, name="PythonCompiler"),
    path("code/webdev", WebCompiler, name="WebCompiler"),
    path("code/python/run", PythonCompile, name="RunCode"),
    path("code/", CodeRedirect, name="Code"), 
]

app_name = "modules"
