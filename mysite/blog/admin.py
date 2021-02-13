"""Admin configuration for blog app."""
from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin site options for Posts."""

    list_display = (
        "title",
        "slug",
        "author",
        "publish",
        "status",
    )
    list_filter = ("status", "created", "publish")
    search_fields = ["title", "author__username"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("author",)
    date_hierarchy = "publish"
    ordering = ("status", "publish")
