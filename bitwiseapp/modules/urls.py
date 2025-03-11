from django.urls import path

from .views import CategoryListView, ModuleDetailView


urlpatterns = [
    path("module/", CategoryListView.as_view(), name="ModuleCategory"),
    path("module/<int:pk", ModuleDetailView, name="Module"),
]

app_name = "modules"