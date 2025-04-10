from django import forms

from .models import Comment, Gallery, Module


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = [
            "title",
            "entry",
            "category",
        ]

    template_name = "module_create_snippet.html"


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "entry",
        ]


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = "__all__"
