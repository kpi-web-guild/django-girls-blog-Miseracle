"""Views for blog app."""

from django.http import HttpResponseRedirect
from .models import Post, Comment
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy, reverse
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
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

    form_class = PostForm
    template_name = 'blog/post_edit.html'

    def form_valid(self, form):
        """Pass request.user to model."""
        form.save(self.request.user)
        return super(NewPost, self).form_valid(form)


class EditPost(UpdateView, Protected):
    """View for editing post."""

    model = Post
    fields = ['title', 'text']
    template_name = 'blog/post_edit.html'


class PostDraftList(ListView, Protected):
    """View for list with unpublished posts."""

    context_object_name = 'posts'
    template_name = 'blog/post_draft_list.html'
    queryset = Post.objects.filter(published_date__isnull=True).order_by('created_date')


class PublishPost(UpdateView, Protected):
    """View for publishing post."""

    def get(self, request, *args, **kwargs):
        """Publish post."""
        post = self.get_object(Post.objects.filter(pk=kwargs['pk']))
        post.publish()
        return HttpResponseRedirect(reverse('post_detail', kwargs={'pk': post.pk}))


class RemovePost(DeleteView, Protected):
    """View for deleting post."""

    model = Post
    success_url = reverse_lazy('post_list')
    template_name = 'blog/post_edit.html'


class AddComment(CreateView):
    """View for adding comment to post."""

    form_class = CommentForm
    template_name = 'blog/add_comment.html'

    def form_valid(self, form):
        """Pass parent post pk to model."""
        post = self.get_object(Post.objects.filter(pk=self.kwargs['pk']))
        form.save(post)
        return super(AddComment, self).form_valid(form)


class ApproveComment(UpdateView, Protected):
    """View for approving comment, if authorized."""

    def get(self, request, *args, **kwargs):
        """Approve comment."""
        comment = self.get_object(Comment.objects.filter(pk=kwargs['pk']))
        comment.approve()
        return HttpResponseRedirect(reverse('post_detail', kwargs={'pk': comment.post.pk}))


class RemoveComment(DeleteView, Protected):
    """View for deleting comment, if authorized."""

    model = Comment
    template_name = 'blog/post_detail.html'

    def get(self, request, *args, **kwargs):
        """Delete comment and return to base post."""
        comment = self.get_object(Comment.objects.filter(pk=kwargs['pk']))
        post_pk = comment.post.pk
        comment.delete()
        return HttpResponseRedirect(reverse('post_detail', kwargs={'pk': post_pk}))
