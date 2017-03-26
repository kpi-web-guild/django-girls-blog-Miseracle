"""Tests for models."""
from datetime import datetime
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from blog.models import Post, Comment


class ModelPostTest(TestCase):
    """Tests for posts."""

    def setUp(self):
        """Test initialization."""
        self.user = User.objects.create(username='testuser')
        self.test_post = Post.objects.create(author=self.user,
                                             title='Test title',
                                             text='Test text')

    def tearDown(self):
        """Clean test data."""
        del self.user
        del self.test_post

    @patch('django.utils.timezone.now', lambda: datetime(day=1,
                                                         month=1,
                                                         year=2017,
                                                         tzinfo=timezone.get_current_timezone()))
    def test_post_publish(self):
        """Post published successfully."""
        self.test_post.publish()
        self.assertEqual(self.test_post.published_date, datetime(day=1,
                                                                 month=1,
                                                                 year=2017,
                                                                 tzinfo=timezone.get_current_timezone()))

    def test_post_rendering(self):
        """Post is rendered as its title."""
        self.assertEqual(str(self.test_post), self.test_post.title)


class ModelCommentTest(TestCase):
    """Tests for comments."""

    def setUp(self):
        """Test initialization."""
        self.user = User.objects.create(username='testuser')
        self.test_post = Post.objects.create(author=self.user, title='Test title', text='Test text')
        self.test_comment = Comment.objects.create(post=self.test_post,
                                                   author=self.user.username,
                                                   text='Test comment text',
                                                   is_approved=False)

    def test_comment_rendering(self):
        """Comment is rendered as its text."""
        self.assertEqual(str(self.test_comment), self.test_comment.text)

    def test_comment_approve(self):
        """Comment approved successfully."""
        self.test_comment.approve()
        self.assertTrue(self.test_comment.is_approved)

    def tearDown(self):
        """Clean test data."""
        del self.user
        del self.test_comment
        del self.test_post
