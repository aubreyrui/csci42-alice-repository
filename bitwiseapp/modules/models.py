from django.db import models
from django.urls import reverse

from accounts.models import Profile


class ModuleCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Module(models.Model):
    title = models.CharField(max_length=255)
    entry = models.TextField()
    author = models.ForeignKey(
        Profile, null=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name="module",
    )
    createdOn = models.DateTimeField(auto_now_add=True, null=True)
    updatedOn = models.DateTimeField(auto_now=True, null=True)
    category = models.ForeignKey(
        "ModuleCategory", on_delete=models.SET_NULL, related_name="modules", null=True
    )

    def __str__(self):
        return "{} from {}".format(self.title, self.category)
    
    def get_absolute_url(self):
        return reverse("modules:Module", args=[self.pk])
    
    class Meta:
        unique_together = [
            ["title", "createdOn"],
            ["title", "entry"]
        ]
        verbose_name = "Module"
        verbose_name_plural = "Modules"

class Comment(models.Model):
    author = models.ForeignKey(
        Profile, null=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name="authoredComment"
    )
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE,
        related_name="comment"
    )
    entry = models.TextField()
    createdOn = models.DateTimeField(auto_now_add=True, null=True)
    updatedOn = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return "comment by {} on {}".format(self.author, self.createdOn)
    
    class Meta:
        ordering = ["-createdOn"]
        unique_together = ["entry", "createdOn"]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


class Gallery(models.Model):
    image = models.ImageField(upload_to="images/", null=True)
    createdOn = models.DateTimeField(auto_now_add=True, null=True)
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="image"
    )
    
    class Meta:
        ordering = ["-createdOn"]
        unique_together = ["image", "createdOn"]
        verbose_name = "Image"
        verbose_name_plural = "Images"