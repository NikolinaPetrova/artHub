from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from artworks.choices import ArtworkTypeChoices
from artworks.models import Artwork
from groups.models import Group, Post, GroupMember
from groups.choices import RoleChoices
from interactions.models import Comment, Like

UserModel = get_user_model()

class LikeViewTests(TestCase):
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
            user=self.user,
            artwork=self.artwork,
        )

        self.post_comment = Comment.objects.create(
            content='Post comment',
            user=self.user,
            post=self.post,
        )

    @patch('interactions.views.NotificationService.notify_like')
    def test_artwork_like_creates_like_and_calls_notification(self, mock_notify):
        self.client.login(username='user1', password='123pass123')
        initial_count = Like.objects.count()
        response = self.client.post(
            reverse('like', kwargs={
                'model_type': 'artwork',
                'pk': self.artwork.pk,
            }),
            HTTP_REFERER=reverse('artwork-details', kwargs={'pk': self.artwork.pk}),
        )

        self.assertRedirects(
            response,
            reverse('artwork-details', kwargs={'pk': self.artwork.pk})
        )
        self.assertEqual(Like.objects.count(), initial_count + 1)

        like = Like.objects.get(user=self.user, artwork=self.artwork)
        self.assertIsNone(like.post)
        self.assertIsNone(like.comment)

        mock_notify.assert_called_once_with(self.artwork, self.user)

    @patch('interactions.views.NotificationService.notify_like')
    def test_second_post_removes_existing_artwork_like(self, mock_notify):
        Like.objects.create(
            user=self.user,
            artwork=self.artwork,
        )

        self.client.login(username='user1', password='123pass123')
        initial_count = Like.objects.count()
        response = self.client.post(
            reverse('like', kwargs={
                'model_type': 'artwork',
                'pk': self.artwork.pk,
            }),
            HTTP_REFERER=reverse('artwork-details', kwargs={'pk': self.artwork.pk}),
        )

        self.assertRedirects(
            response,
            reverse('artwork-details', kwargs={'pk': self.artwork.pk})
        )
        self.assertEqual(Like.objects.count(), initial_count - 1)
        self.assertFalse(
            Like.objects.filter(user=self.user, artwork=self.artwork).exists()
        )

        mock_notify.assert_not_called()

    @patch('interactions.views.NotificationService.notify_like')
    def test_group_member_can_like_post(self, mock_notify):
        GroupMember.objects.create(
            user=self.user,
            group=self.group,
            role=RoleChoices.MEMBER,
        )

        self.client.login(username='user1', password='123pass123')
        initial_count = Like.objects.count()

        response = self.client.post(
            reverse('like', kwargs={
                'model_type': 'post',
                'pk': self.post.pk,
            }),
            HTTP_REFERER=reverse('post-details', kwargs={
                'slug': self.group.slug,
                'pk': self.post.pk,
            }),
        )

        self.assertRedirects(
            response,
            reverse('post-details', kwargs={
                'slug': self.group.slug,
                'pk': self.post.pk,
            })
        )
        self.assertEqual(Like.objects.count(), initial_count + 1)
        self.assertTrue(
            Like.objects.filter(user=self.user, post=self.post).exists()
        )

        mock_notify.assert_called_once_with(self.post, self.user)

    @patch('interactions.views.NotificationService.notify_like')
    def test_non_member_cannot_like_post(self, mock_notify):
        self.client.login(username='user2', password='123pass123')
        initial_count = Like.objects.count()

        response = self.client.post(
            reverse('like', kwargs={
                'model_type': 'post',
                'pk': self.post.pk,
            }),
            HTTP_REFERER=reverse('post-details', kwargs={
                'slug': self.group.slug,
                'pk': self.post.pk,
            }),
        )

        self.assertRedirects(
            response,
            reverse('group-details', kwargs={'slug': self.group.slug})
        )
        self.assertEqual(Like.objects.count(), initial_count)
        self.assertFalse(
            Like.objects.filter(user=self.other_user, post=self.post).exists()
        )

        mock_notify.assert_not_called()

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any('You must be a group member to like posts.' in str(message) for message in messages)
        )

    @patch('interactions.views.NotificationService.notify_like')
    def test_non_member_cannot_like_comment_on_post(self, mock_notify):
        self.client.login(username='user2', password='123pass123')
        initial_count = Like.objects.count()

        response = self.client.post(
            reverse('like', kwargs={
                'model_type': 'comment',
                'pk': self.post_comment.pk,
            }),
            HTTP_REFERER=reverse('post-details', kwargs={
                'slug': self.group.slug,
                'pk': self.post.pk,
            }),
        )

        self.assertRedirects(
            response,
            reverse('group-details', kwargs={'slug': self.group.slug})
        )
        self.assertEqual(Like.objects.count(), initial_count)
        self.assertFalse(
            Like.objects.filter(user=self.other_user, comment=self.post_comment).exists()
        )

        mock_notify.assert_not_called()

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any('You must be a group member to like comments on posts.' in str(message) for message in messages)
        )

    @patch('interactions.views.NotificationService.notify_like')
    def test_like_comment_on_artwork_creates_like_and_calls_notification(self, mock_notify):
        self.client.login(username='user1', password='123pass123')
        initial_count = Like.objects.count()

        response = self.client.post(
            reverse('like', kwargs={
                'model_type': 'comment',
                'pk': self.artwork_comment.pk,
            }),
            HTTP_REFERER=reverse('artwork-details', kwargs={'pk': self.artwork.pk}),
        )

        self.assertRedirects(
            response,
            reverse('artwork-details', kwargs={'pk': self.artwork.pk})
        )
        self.assertEqual(Like.objects.count(), initial_count + 1)
        self.assertTrue(
            Like.objects.filter(user=self.user, comment=self.artwork_comment).exists()
        )

        mock_notify.assert_called_once_with(self.artwork_comment, self.user)

    def test_invalid_model_type_redirects_to_home(self):
        self.client.login(username='user1', password='123pass123')
        initial_count = Like.objects.count()

        response = self.client.post(
            reverse('like', kwargs={
                'model_type': 'invalid-type',
                'pk': 999,
            }),
            HTTP_REFERER=reverse('home'),
        )

        self.assertRedirects(response, reverse('home'))
        self.assertEqual(Like.objects.count(), initial_count)