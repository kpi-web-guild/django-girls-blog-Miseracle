"""Blog views.

- post_list - returns post list;
"""

from django.conf.urls import url
from . import views
from django.contrib import admin

urlpatterns = [
    url(r'^$', views.PostListView.as_view(), name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.PostDetailView.as_view(), name='post_detail'),
    url(r'^post/new/$', views.NewPost.as_view(), name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.EditPost.as_view(), name='post_edit'),
    url(r'^drafts/$', views.PostDraftList.as_view(), name='post_draft_list'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.PublishPost.as_view(), name='post_publish'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.RemovePost.as_view(), name='post_remove'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.AddComment.as_view(), name='add_comment'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.ApproveComment.as_view(), name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.RemoveComment.as_view(), name='comment_remove'),
    url(r'^admin/', admin.site.urls),
]
