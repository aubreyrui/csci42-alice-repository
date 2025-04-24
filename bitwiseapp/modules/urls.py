from django.urls import path

from .views import CategoryListView, ModuleDetailView, ModuleCreateView, ModuleUpdateView
from .views import ModuleDeleteView, CommentDeleteView, GalleryDeleteView
from .views import Execute, Compiler, Compile


urlpatterns = [
    path("list/", CategoryListView.as_view(), name="ModuleCategory"),
    path("lesson/<int:pk>", ModuleDetailView, name="Module"),
    path("lesson/add", ModuleCreateView, name="ModuleCreate"),
    path("lesson/<int:pk>/edit", ModuleUpdateView.as_view(), name="ModuleUpdate"),
    path("lesson/<int:pk>/delete", ModuleDeleteView, name="ModuleDelete"),
    path("lesson/<int:pk>/comment/delete", CommentDeleteView, name="CommentDelete"),
    path("lesson/<int:pk>/gallery/delete", GalleryDeleteView, name="GalleryDelete"),
    path("compiler", Compiler, name="Compiler"), 
    path("compiler/run", Compile, name="RunCode"),
]

app_name = "modules"