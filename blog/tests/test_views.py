"""Tests for views."""
from datetime import datetime
from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.utils import timezone

from blog.models import Post, Comment


class ViewsTest(TestCase):
    """Tests for views."""

    USERNAME = 'testuser'
    PASSWORD = 'password'

    def setUp(self):
        """Init test data."""
        self.client = Client()
        self.user = User.objects.create(username=self.USERNAME,
                                        email='testuser@test.com',
                                        is_superuser=True,
                                        is_staff=True,
                                        is_active=True)
        self.user.set_password(self.PASSWORD)
        self.user.save()

    def tearDown(self):
        """Clean test data."""
        del self.client
        del self.user

    def test_index_rendering(self):
        """Test post list rendering."""
        tz = timezone.get_current_timezone()
        post = Post.objects.create(author=self.user, title='Test', text='superText',
                                   created_date=datetime(day=1, month=3, year=2016, tzinfo=tz),
                                   published_date=datetime(day=1, month=3, year=2016, tzinfo=tz))
        past_post = Post.objects.create(author=self.user, title='past_test', text='superText',
                                        created_date=datetime(day=1, month=4, year=2015, tzinfo=tz),
                                        published_date=datetime(day=1, month=4, year=2015, tzinfo=tz))
        future_post = Post.objects.create(author=self.user, title='future_test', text='superText',
                                          created_date=datetime(day=1, month=4, year=2116, tzinfo=tz),
                                          published_date=datetime(day=1, month=4, year=2116, tzinfo=tz))
        with patch('django.utils.timezone.now', lambda: datetime(day=1, month=1, year=2016, tzinfo=tz)):
            response = self.client.get(reverse('post_list'))
            self.assertListEqual(list(response.context['posts']), [past_post])
            self.assertNotContains(response, post)
            self.assertNotContains(response, future_post)
        with patch('django.utils.timezone.now', lambda: datetime(day=1, month=4, year=2016, tzinfo=tz)):
            response = self.client.get(reverse('post_list'))
            self.assertListEqual(list(response.context['posts']), [past_post, post])
            self.assertNotContains(response, future_post)
        with patch('django.utils.timezone.now', lambda: datetime(day=1, month=4, year=3016, tzinfo=tz)):
            response = self.client.get(reverse('post_list'))
            self.assertListEqual(list(response.context['posts']), [past_post, post, future_post])
        response = self.client.get(reverse('post_list'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'blog/post_list.html', 'blog/base.html')
        self.assertContains(response, post)
        self.assertContains(response, past_post)
        self.assertNotContains(response, future_post)

    def test_detail_view(self):
        """Testing detail page when post is not exist and when it exists."""
        response = self.client.get(reverse('post_detail', kwargs={'pk': 1}))
        self.assertEqual(404, response.status_code)
        post = Post.objects.create(author=self.user, title='Test', text='superText')
        response = self.client.get(reverse('post_detail', kwargs={'pk': post.pk}))
        self.assertEqual(200, response.status_code)

    def test_post_new_view(self):
        """Testing new post view: before and after login; post creating."""
        response = self.client.get(reverse('post_new'))
        self.assertEqual(302, response.status_code)
        authorization = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertTrue(authorization)
        response = self.client.post(reverse('post_new'), {'author': self.user, 'title': 'Test', 'text': 'superText', },
                                    follow=True)
        self.assertEqual(200, response.status_code)
        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': 1}))
        response = self.client.get(reverse('post_draft_list'), follow=True)
        self.post = Post.objects.get(author=self.user, title='Test', text='superText')
        self.assertContains(response, self.post)

    def test_post_edit(self):
        """Testing edit views before and after user login."""
        response = self.client.get(reverse('post_edit', kwargs={'pk': 1}))
        self.assertEqual(302, response.status_code)
        authorization = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertTrue(authorization)
        response = self.client.get(reverse('post_edit', kwargs={'pk': 1}))
        self.assertEqual(404, response.status_code)
        post = Post.objects.create(author=self.user, title='Test', text='superText')
        response = self.client.get(reverse('post_edit', kwargs={'pk': post.pk}))
        self.assertEqual(200, response.status_code)

    def test_drafts(self):
        """Testing drafts view before and after login."""
        response = self.client.get(reverse('post_draft_list'))
        self.assertEqual(302, response.status_code)
        authorization = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertTrue(authorization)
        response = self.client.get(reverse('post_draft_list'))
        self.assertEqual(200, response.status_code)

    def test_publish_post(self):
        """Testing publishing post: before login and after; visibility only after publishing."""
        response = self.client.get(reverse('post_publish', kwargs={'pk': 1}))
        self.assertEqual(302, response.status_code)

        authorization = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertTrue(authorization)
        response = self.client.get(reverse('post_publish', kwargs={'pk': 1}))
        self.assertEqual(404, response.status_code)
        post = Post.objects.create(author=self.user, title='Test', text='superText')

        self.client.logout()
        response = self.client.get(reverse('post_list'), follow=True)
        self.assertNotContains(response, post)

        authorization = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertTrue(authorization)
        response = self.client.get(reverse('post_publish', kwargs={'pk': post.pk}), follow=True)
        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': post.pk}))
        response = self.client.get(reverse('post_list'), follow=True)
        self.assertContains(response, post)

    def test_delete_post(self):
        """Testing deleting post: before and after login; post deleting."""
        response = self.client.get(reverse('post_remove', kwargs={'pk': 1}))
        self.assertEqual(302, response.status_code)
        authorization = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertTrue(authorization)
        response = self.client.get(reverse('post_remove', kwargs={'pk': 1}))
        self.assertEqual(404, response.status_code)
        post = Post.objects.create(author=self.user, title='Tst', text='superText')
        other_post = Post.objects.create(author=self.user, title='Test_other', text='Other text')
        response = self.client.get(reverse('post_remove', kwargs={'pk': post.pk}), follow=True)
        self.assertRedirects(response, reverse('post_list'))
        response = self.client.get(reverse('post_draft_list'), follow=True)
        self.assertNotContains(response, post)
        self.assertContains(response, other_post)

    def test_add_comment(self):
        """Testing adding comment to post."""
        self.post = Post.objects.create(author=self.user, title='Test', text='superText')
        response = self.client.get(reverse('add_comment', kwargs={'pk': self.post.pk}))
        self.assertEqual(200, response.status_code)
        response = self.client.post(reverse('add_comment', kwargs={'pk': self.post.pk}),
                                    {'author': self.user, 'text': 'Super'}, follow=True)
        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': self.post.pk}))

    def test_comment_approve(self):
        """Testing comment approve view: comment visibility only after approving."""
        self.post = Post.objects.create(author=self.user, title='Test', text='superText')
        self.comment = Comment.objects.create(post=self.post, author=self.user, text='superComment')
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}), follow=True)
        self.assertNotContains(response, self.comment)
        authorization = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertTrue(authorization)
        response = self.client.get(reverse('comment_approve', kwargs={'pk': self.comment.pk}), follow=True)
        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': self.post.pk}))
        self.client.logout()
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}), follow=True)
        self.assertContains(response, self.comment)

    def test_comment_delete(self):
        """Testing delete comment view."""
        response = self.client.get(reverse('post_remove', kwargs={'pk': 1}))
        self.assertEqual(302, response.status_code)
        authorization = self.client.login(username=self.USERNAME, password=self.PASSWORD)
        self.assertTrue(authorization)
        response = self.client.get(reverse('post_remove', kwargs={'pk': 1}))
        self.assertEqual(404, response.status_code)
        self.post = Post.objects.create(author=self.user, title='Test', text='superText')
        self.comment = Comment.objects.create(post=self.post, author=self.user, text='superComment')
        self.other_comment = Comment.objects.create(post=self.post, author=self.user, text='AnotherComment')
        response = self.client.get(reverse('comment_remove', kwargs={'pk': self.comment.pk}), follow=True)
        self.assertRedirects(response, reverse('post_detail', kwargs={'pk': self.post.pk}))
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}), follow=True)
        self.assertNotContains(response, self.comment)
        self.assertContains(response, self.other_comment)
