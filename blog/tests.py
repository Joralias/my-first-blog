from django.test import TestCase
from .models import Post, Comment
from django.utils import timezone
import datetime
from django.contrib.auth.models import User


class PostTestCase(TestCase):
    def setUp(self):
        """ Creation of User, Post and comment for following tests"""
        user = User.objects.create(username="TestUser", password="TestPass")
        date = datetime.datetime(2009, 10, 5, 18, 00)
        post = Post.objects.create(author=user, title="TestPost", text="PostText", published_date=date)
        Comment.objects.create(post=post, text="Test comment approved", author="CommentAuthor", approved_comment=True)
        Comment.objects.create(post=post, text="Test comment not approved", author="CommentAuthor")

    def test_approved_comments(self):
        """Test approved comments of a Post"""
        post = Post.objects.get(title="TestPost")
        comment = Comment.objects.get(text="Test comment approved")
        self.assertEqual(post.approved_comments().first(), comment)

    def test_publish(self):
        """Publish date is correctly set"""
        post = Post.objects.get(title="TestPost")
        post.publish()
        time = timezone.now()
        self.assertEqual(post.published_date, time)


class CommentTestCase(TestCase):
    def setUp(self):
        """ Creation of User, Post and comment for following tests"""
        user = User.objects.create(username="TestUser", password="TestPass")
        date = datetime.datetime(2009, 10, 5, 18, 00)
        post = Post.objects.create(author=user, title="TestPost", text="PostText", published_date=date)
        Comment.objects.create(post=post, text="Test comment not approved", author="CommentAuthor")

    def test_approve(self):
        """Approve a comment"""
        comment = Comment.objects.get(text="Test comment not approved")
        comment.approve()
        self.assertTrue(comment.approved_comment)
