"""DB models.

- Post - represents a post in a blog;
"""

from django.db import models
from django.utils import timezone


class Post(models.Model):
    """Represent a post in a blog.

    Fields: author, title, text, created_date, published_date
    Methods: publish, __str__
    """

    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        """Publish this post."""
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        """Show post title."""
        return self.title
