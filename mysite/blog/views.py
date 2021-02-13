"""Views for blog app."""
from typing import Any, Dict

from django.core.mail import send_mail
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView

from .forms import EmailPostForm
from .models import Post


class PostListView(ListView):
    """List the published posts.  Implement view as a class."""

    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/list.html"


def post_detail(
    request: HttpRequest, year: int, month: int, day: int, post: Post
) -> HttpResponse:
    """Display details about the provided post."""
    post = get_object_or_404(
        Post,
        slug=post,
        status="published",
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(request, "blog/detail.html", context={"post": post})


def post_share(request: HttpRequest, post_id: int) -> HttpResponse:
    """Share post via email."""
    # Retrieve post by ID
    post: Post = get_object_or_404(Post, id=post_id, status="published")
    sent: bool = False
    if request.method == "POST":
        form: EmailPostForm = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cleaned_data: Dict[str, Any] = form.cleaned_data
            post_url: str = request.build_absolute_uri(post.get_absolute_url())
            subject: str = f"{cleaned_data['name']} recommends you read {post.title}"
            message: str = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cleaned_data['name']}'s comments: {cleaned_data['comments']}"
            )
            send_mail(subject, message, cleaned_data["email"], [cleaned_data["to"]])
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request, "blog/share.html", {"post": post, "form": form, "sent": sent}
    )
