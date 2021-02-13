"""Model definitions for the blog app."""
from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from django.urls.base import reverse
from django.utils import timezone


class PublishedManager(models.Manager):
    """PublishedManager - QueryManager for only published posts."""

    def get_queryset(self) -> QuerySet:
        """Return queryset consisting of only published posts."""
        return super().get_queryset().filter(status="published")


class Post(models.Model):
    """Data model for blog post."""

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts"
    )
    body: models.TextField = models.TextField()
    publish: models.DateTimeField = models.DateTimeField(default=timezone.now)
    created: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated: models.DateTimeField = models.DateTimeField(auto_now=True)
    status: models.CharField = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="draft"
    )

    # Query Managers
    # - first manager found is the default manager
    # - need to define 'objects' because we have multiple managers and we need to keep the 'objects' manager
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        """Metadata options for Post model."""

        ordering = ("-publish",)

    def __str__(self) -> str:
        """Return blog post title when accessing post as a string."""
        return self.title

    def get_absolute_url(self) -> str:
        """Return absolute URL for a blog post."""
        return reverse(
            "blog:post_detail",
            kwargs={
                "year": self.publish.year,
                "month": self.publish.month,
                "day": self.publish.day,
                "post": self.slug,
            },
        )
