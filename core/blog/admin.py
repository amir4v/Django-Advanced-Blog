from django.contrib import admin
from .models import Category, Post


class PostModelAdmin(admin.ModelAdmin):
    list_display = [
        "author",
        "title",
        "status",
        "category",
        "created_dt",
        "published_dt",
    ]


admin.site.register(Category)
admin.site.register(Post, PostModelAdmin)
