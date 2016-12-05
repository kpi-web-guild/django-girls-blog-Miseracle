"""Views for blog app.

- post_list - returns post list;
"""

from django.shortcuts import render
from .models import Post
from django.utils import timezone
# Create your views here.


def post_list(request):
    """Show posts, which are published, ordered by published date."""
    posts = (
        Post.objects
        .filter(published_date__lte=timezone.now())
        .order_by('published_date')
    )
    return render(request, 'blog/post_list.html', {'posts': posts})
