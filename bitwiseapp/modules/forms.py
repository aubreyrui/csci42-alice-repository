from django import forms

from .models import Module, Comment, Gallery


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ["title", "entry", "category", ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["entry",]

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = "__all__"