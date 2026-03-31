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

class ReplyCommentViewTests(TestCase):
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

    @patch('interactions.views.NotificationService.notify_comment')
    def test_valid_reply_to_artwork_comment_creates_reply_and_calls_notification(self, mock_notify):
        self.client.login(username='user1', password='123pass123')
        initial_count = Comment.objects.count()

        response = self.client.post(
            reverse('reply-comment', kwargs={'pk': self.artwork_comment.pk}),
            data={'content': 'Reply to artwork comment'},
            HTTP_REFERER=reverse('artwork-details', kwargs={'pk': self.artwork.pk}),
        )

        self.assertRedirects(
            response,
            reverse('artwork-details', kwargs={'pk': self.artwork.pk})
        )
        self.assertEqual(Comment.objects.count(), initial_count + 1)

        reply = Comment.objects.get(
            user=self.user,
            parent=self.artwork_comment,
            content='Reply to artwork comment',
        )
        self.assertEqual(reply.artwork, self.artwork)
        self.assertIsNone(reply.post)

        mock_notify.assert_called_once_with(reply)

    @patch('interactions.views.NotificationService.notify_comment')
    def test_valid_reply_to_post_comment_by_group_member_creates_reply_and_calls_notification(self, mock_notify):
        GroupMember.objects.create(
            user=self.user,
            group=self.group,
            role=RoleChoices.MEMBER,
        )

        self.client.login(username='user1', password='123pass123')
        initial_count = Comment.objects.count()

        response = self.client.post(
            reverse('reply-comment', kwargs={'pk': self.post_comment.pk}),
            data={'content': 'Reply to post comment'},
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

        reply = Comment.objects.get(
            user=self.user,
            parent=self.post_comment,
            content='Reply to post comment',
        )
        self.assertEqual(reply.post, self.post)
        self.assertIsNone(reply.artwork)

        mock_notify.assert_called_once_with(reply)

    @patch('interactions.views.NotificationService.notify_comment')
    def test_reply_to_post_comment_by_non_member_does_not_create_reply_and_shows_message(self, mock_notify):
        self.client.login(username='user2', password='123pass123')
        initial_count = Comment.objects.count()

        response = self.client.post(
            reverse('reply-comment', kwargs={'pk': self.post_comment.pk}),
            data={'content': 'Unauthorized reply'},
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
                parent=self.post_comment,
                content='Unauthorized reply',
            ).exists()
        )

        mock_notify.assert_not_called()

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any('You must be a group member to reply to comments.' in str(message) for message in messages)
        )

    @patch('interactions.views.NotificationService.notify_comment')
    def test_invalid_form_does_not_create_reply_and_does_not_call_notification(self, mock_notify):
        self.client.login(username='user1', password='123pass123')
        initial_count = Comment.objects.count()

        response = self.client.post(
            reverse('reply-comment', kwargs={'pk': self.artwork_comment.pk}),
            data={'content': '      '},
            HTTP_REFERER=reverse('artwork-details', kwargs={'pk': self.artwork.pk}),
        )

        self.assertRedirects(
            response,
            reverse('artwork-details', kwargs={'pk': self.artwork.pk})
        )
        self.assertEqual(Comment.objects.count(), initial_count)

        mock_notify.assert_not_called()