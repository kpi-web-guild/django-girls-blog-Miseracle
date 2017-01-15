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

    @property
    def approved_comments(self):
        """Return all approved (published) comments."""
        return self.comments.filter(is_approved=True)


class Comment(models.Model):
    """Represents a comment to post."""

    post = models.ForeignKey('Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False)

    def approve(self):
        """Approve comment."""
        self.is_approved = True
        self.save()

    def __str__(self):
        """Represent a comment as a string by its text."""
        return self.text
