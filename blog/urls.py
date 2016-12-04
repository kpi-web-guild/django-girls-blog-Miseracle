"""Blog views.

- post_list - returns post list;
"""

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
]
