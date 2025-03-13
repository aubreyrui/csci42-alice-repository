from django.urls import path

from .views import CategoryListView, ModuleDetailView, ModuleCreateView, ModuleUpdateView, GalleryCreateView


urlpatterns = [
    path("list/", CategoryListView.as_view(), name="ModuleCategory"),
    path("lesson/<int:pk>", ModuleDetailView, name="Module"),
    path("lesson/add", ModuleCreateView, name="ModuleCreate"),
    path("lesson/<int:pk>/edit", ModuleUpdateView.as_view(), name="ModuleUpdate"),
    path("lesson/<int:pk>/newgallery", GalleryCreateView.as_view(), name="Gallery"),
]

app_name = "modules"