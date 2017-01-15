"""Form class."""

from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Main form for Post."""

    class Meta:
        """Metadata for post form."""

        model = Post
        fields = ('title', 'text',)


class CommentForm(forms.ModelForm):
    """Main form for comment."""

    class Meta:
        """Metadata for comment form."""

        model = Comment
        fields = ('author', 'text',)
