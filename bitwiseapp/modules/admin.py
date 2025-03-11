from django.contrib import admin

from .models import Module, ModuleCategory, Comment, Gallery


class ModuleInline(admin.TabularInline):
    model = Module


class CategoryAdmin(admin.ModelAdmin):
    model = ModuleCategory
    inlines = [ModuleInline,]

    search_fields = ["name",]
    list_display = ["name", "description"]

class GalleryInline(admin.TabularInline):
    model = Gallery

class CommentInline(admin.TabularInline):
    model = Comment

class ModuleAdmin(admin.ModelAdmin):
    model = Module
    inline = [CommentInline, GalleryInline]

    search_fields = ["title",]

    list_display = ["category", "title", "updatedOn"]
    list_filter = ["category"]

    fieldsets = [("Details", {
        "fields": [("category", "title"), "entry"]
    })]

class GalleryAdmin(admin.ModelAdmin):
    model = Gallery

class CommentAdmin(admin.ModelAdmin):
    model = Comment

    list_display = ["article", "author"]

admin.site.register(Module, ModuleAdmin)
admin.site.register(ModuleCategory, CategoryAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Comment, CommentAdmin)