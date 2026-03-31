from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from artworks.choices import ArtworkTypeChoices
from artworks.models import Artwork
from groups.models import Group, Post
from interactions.models import Comment

UserModel = get_user_model()

class CommentDeleteViewTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='123pass123',
        )
        self.other_user = UserModel.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='123pass123',
        )
        self.third_user = UserModel.objects.create_user(
            username='user3',
            email='user3@test.com',
            password='123pass123',
        )

        self.artwork = Artwork.objects.create(
            title='Test artwork',
            description='desc',
            image_url='https://example.com/image.jpg',
            type=ArtworkTypeChoices.PAINTING,
            user=self.user,
        )

        self.group = Group.objects.create(
            name='Test Group',
            slug='test-group',
            owner=self.user,
        )

        self.post = Post.objects.create(
            group=self.group,
            author=self.user,
            content='Test post content',
        )

        self.artwork_comment = Comment.objects.create(
            content='Artwork comment',
            user=self.other_user,
            artwork=self.artwork,
        )

        self.post_comment = Comment.objects.create(
            content='Post comment',
            user=self.other_user,
            post=self.post,
        )

    def test_comment_owner_can_delete_comment(self):
        own_comment = Comment.objects.create(
            content='My own comment',
            user=self.user,
            artwork=self.artwork,
        )

        self.client.login(username='user1', password='123pass123')
        response = self.client.post(
            reverse('delete-comment', kwargs={'pk': own_comment.pk})
        )

        self.assertRedirects(
            response,
            reverse('artwork-details', kwargs={'pk': self.artwork.pk})
        )
        self.assertFalse(Comment.objects.filter(pk=own_comment.pk).exists())

    def test_artwork_owner_can_delete_comment_on_artwork(self):
        self.client.login(username='user1', password='123pass123')
        response = self.client.post(
            reverse('delete-comment', kwargs={'pk': self.artwork_comment.pk})
        )

        self.assertRedirects(
            response,
            reverse('artwork-details', kwargs={'pk': self.artwork.pk})
        )
        self.assertFalse(Comment.objects.filter(pk=self.artwork_comment.pk).exists())

    def test_post_author_can_delete_comment_on_post(self):
        self.client.login(username='user1', password='123pass123')
        response = self.client.post(
            reverse('delete-comment', kwargs={'pk': self.post_comment.pk})
        )

        self.assertRedirects(
            response,
            reverse('post-details', kwargs={'slug': self.group.slug, 'pk': self.post.pk})
        )
        self.assertFalse(Comment.objects.filter(pk=self.post_comment.pk).exists())

    def test_user_with_permission_can_delete_comment(self):
        permission = Permission.objects.get(codename='delete_comment')
        self.third_user.user_permissions.add(permission)
        self.client.login(username='user3', password='123pass123')
        response = self.client.post(
            reverse('delete-comment', kwargs={'pk': self.artwork_comment.pk})
        )

        self.assertRedirects(
            response,
            reverse('artwork-details', kwargs={'pk': self.artwork.pk})
        )
        self.assertFalse(Comment.objects.filter(pk=self.artwork_comment.pk).exists())

    def test_user_without_permission_cannot_delete_comment(self):
        self.client.login(username='user3', password='123pass123')
        response = self.client.post(
            reverse('delete-comment', kwargs={'pk': self.artwork_comment.pk})
        )

        self.assertRedirects(response, reverse('home'))
        self.assertTrue(Comment.objects.filter(pk=self.artwork_comment.pk).exists())

    def test_comment_without_artwork_or_post_redirects_to_home_after_delete(self):
        own_comment = Comment.objects.create(
            content='Standalone comment',
            user=self.user,
        )
        self.client.login(username='user1', password='123pass123')
        response = self.client.post(
            reverse('delete-comment', kwargs={'pk': own_comment.pk})
        )

        self.assertRedirects(response, reverse('home'))
        self.assertFalse(Comment.objects.filter(pk=own_comment.pk).exists())