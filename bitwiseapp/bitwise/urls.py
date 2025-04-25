from django.urls import path

from .views import HomepageView

urlpatterns = [
    path("", HomepageView, name="index"),
]

app_name = "bitwise"
