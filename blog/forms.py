"""Form class."""

from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Main form for Post."""

    class Meta:
        """Metadata for post form."""

        model = Post
        fields = ('title', 'text',)

    def save(self, user=None):
        """Save post to DB, assigning author field."""
        post = super().save(commit=False)
        if user:
            post.author = user
            post.save()
        return post


class CommentForm(forms.ModelForm):
    """Main form for comment."""

    class Meta:
        """Metadata for comment form."""

        model = Comment
        fields = ('author', 'text',)

    def save(self, post=None):
        """Save comment to DB, assigning post (parent) field."""
        comment = super().save(commit=False)
        if post:
            comment.post = post
            comment.save()
        return comment
