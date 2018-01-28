"""Views for blog app.

- post_list - returns post list;
"""

from django.shortcuts import get_object_or_404, redirect
from .models import Post, Comment
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
# Create your views here.


class Protected(View):
    """Deny access to view for unauthorized users."""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        """Call base method with login_required extension."""
        return super().dispatch(*args, **kwargs)


class PostListView(ListView):
    """View for list of all published posts."""

    context_object_name = 'posts'
    template_name = 'blog/post_list.html'

    def get_queryset(self):
        """Return already published posts."""
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')


class PostDetailView(DetailView):
    """View with detail info about post."""

    model = Post
    template_name = 'blog/post_detail.html'


class NewPost(CreateView, Protected):
    """View for creating new post."""

    model = Post
    fields = ['title', 'text']
    template_name = 'blog/post_edit.html'

    def post(self, request, *args, **kwargs):
        """Get author-field from request and save post to DB."""
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)


class EditPost(UpdateView, Protected):
    """View for editing post."""

    model = Post
    fields = ['title', 'text']
    template_name = 'blog/post_edit.html'

    def get_success_url(self):
        """Return to detail view of edited post."""
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})


class PostDraftList(ListView, Protected):
    """View for list with unpublished posts."""

    context_object_name = 'posts'
    template_name = 'blog/post_draft_list.html'
    queryset = Post.objects.filter(published_date__isnull=True).order_by('created_date')


class PublishPost(TemplateView, Protected):
    """View for publishing post."""

    def get(self, request, *args, **kwargs):
        """Publish post."""
        post = get_object_or_404(Post, pk=kwargs['pk'])
        post.publish()
        return redirect('post_detail', pk=post.pk)


class RemovePost(DeleteView, Protected):
    """View for deleting post."""

    model = Post
    success_url = reverse_lazy('post_list')
    template_name = 'blog/post_edit.html'


class AddComment(CreateView):
    """View for adding comment to post."""

    model = Comment
    fields = ['author', 'text']
    template_name = 'blog/add_comment.html'

    def post(self, request, *args, **kwargs):
        """Save new comment to DB."""
        post = get_object_or_404(Post, pk=kwargs['pk'])
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)


class ApproveComment(TemplateView, Protected):
    """View for approving comment, if authorized."""

    def get(self, request, *args, **kwargs):
        """Approve comment."""
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        comment.approve()
        return redirect('post_detail', pk=comment.post.pk)


class RemoveComment(DeleteView, Protected):
    """View for deleting comment, if authorized."""

    model = Comment
    template_name = 'blog/post_detail.html'

    def get(self, request, *args, **kwargs):
        """Delete comment and return to base post."""
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        post_pk = comment.post.pk
        comment.delete()
        return redirect('post_detail', pk=post_pk)
