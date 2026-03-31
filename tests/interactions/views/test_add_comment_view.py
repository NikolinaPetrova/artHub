from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from artworks.choices import ArtworkTypeChoices
from artworks.models import Artwork
from groups.models import Group, Post, GroupMember
from groups.choices import RoleChoices
from interactions.models import Comment

UserModel = get_user_model()


class AddCommentViewTests(TestCase):
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

    @patch('interactions.views.NotificationService.notify_comment')
    def test_valid_artwork_comment_creates_comment_and_calls_notification(self, mock_notify):
        self.client.login(username='user1', password='123pass123')
        initial_count = Comment.objects.count()

        response = self.client.post(
            reverse('add-comment', kwargs={
                'model_type': 'artwork',
                'pk': self.artwork.pk,
            }),
            data={'content': 'Nice artwork!'},
            HTTP_REFERER=reverse('artwork-details', kwargs={'pk': self.artwork.pk}),
        )

        self.assertRedirects(
            response,
            reverse('artwork-details', kwargs={'pk': self.artwork.pk})
        )
        self.assertEqual(Comment.objects.count(), initial_count + 1)

        comment = Comment.objects.get(
            user=self.user,
            artwork=self.artwork,
            content='Nice artwork!',
        )
        self.assertIsNone(comment.post)

        mock_notify.assert_called_once_with(comment)

    @patch('interactions.views.NotificationService.notify_comment')
    def test_valid_post_comment_by_group_member_creates_comment_and_calls_notification(self, mock_notify):
        GroupMember.objects.create(
            user=self.user,
            group=self.group,
            role=RoleChoices.MEMBER,
        )

        self.client.login(username='user1', password='123pass123')
        initial_count = Comment.objects.count()

        response = self.client.post(
            reverse('add-comment', kwargs={
                'model_type': 'post',
                'pk': self.post.pk,
            }),
            data={'content': 'Nice post!'},
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
        self.assertEqual(Comment.objects.count(), initial_count + 1)

        comment = Comment.objects.get(
            user=self.user,
            post=self.post,
            content='Nice post!',
        )
        self.assertIsNone(comment.artwork)

        mock_notify.assert_called_once_with(comment)

    @patch('interactions.views.NotificationService.notify_comment')
    def test_post_comment_by_non_member_does_not_create_comment_and_shows_message(self, mock_notify):
        self.client.login(username='user2', password='123pass123')
        initial_count = Comment.objects.count()

        response = self.client.post(
            reverse('add-comment', kwargs={
                'model_type': 'post',
                'pk': self.post.pk,
            }),
            data={'content': 'I should not comment'},
            HTTP_REFERER=reverse('post-details', kwargs={
                'slug': self.group.slug,
                'pk': self.post.pk,
            }),
        )

        self.assertRedirects(
            response,
            reverse('group-details', kwargs={'slug': self.group.slug})
        )
        self.assertEqual(Comment.objects.count(), initial_count)
        self.assertFalse(
            Comment.objects.filter(
                user=self.other_user,
                post=self.post,
                content='I should not comment',
            ).exists()
        )

        mock_notify.assert_not_called()

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any('You must be a group member to comment on posts.' in str(message) for message in messages)
        )

    @patch('interactions.views.NotificationService.notify_comment')
    def test_invalid_form_does_not_create_comment_and_does_not_call_notification(self, mock_notify):
        self.client.login(username='user1', password='123pass123')
        initial_count = Comment.objects.count()

        response = self.client.post(
            reverse('add-comment', kwargs={
                'model_type': 'artwork',
                'pk': self.artwork.pk,
            }),
            data={'content': '      '},
            HTTP_REFERER=reverse('artwork-details', kwargs={'pk': self.artwork.pk}),
        )

        self.assertRedirects(
            response,
            reverse('artwork-details', kwargs={'pk': self.artwork.pk})
        )
        self.assertEqual(Comment.objects.count(), initial_count)
        self.assertFalse(
            Comment.objects.filter(
                user=self.user,
                artwork=self.artwork,
                content='',
            ).exists()
        )

        mock_notify.assert_not_called()