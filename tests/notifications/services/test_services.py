from django.contrib.auth import get_user_model
from django.test import TestCase
from artworks.models import Artwork
from groups.choices import RoleChoices
from groups.models import Group, GroupMember, Post
from interactions.models import Comment
from notifications.models import Notification
from notifications.services import NotificationService

UserModel = get_user_model()


class NotificationServiceTests(TestCase):
    def setUp(self):
        self.user1 = UserModel.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='123pass123'
        )

        self.user2 = UserModel.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='123pass123'
        )

        self.user3 = UserModel.objects.create_user(
            username='user3',
            email='user3@test.com',
            password='123pass123'
        )

        self.artwork = Artwork.objects.create(
            title='Test artwork',
            image_url = 'https://example.com/artwork.jpg',
            user=self.user1
        )

        self.group = Group.objects.create(
            name='Test group',
            slug='test-group',
            owner=self.user1,
        )

    def test_get_artwork_url(self):
        url = NotificationService.get_artwork_url(self.artwork)
        self.assertIn(str(self.artwork.pk), url)

    def test_get_group_url_with_tab(self):
        url = NotificationService.get_group_url(self.group, tab='members')
        self.assertIn('?tab=members', url)

    def test_create_if_not_sender_creates_notification(self):
        NotificationService.create_if_not_sender(
            recipient=self.user1,
            sender=self.user2,
            notification_type='test',
            message='test',
        )

        self.assertEqual(Notification.objects.count(), 1)

    def test_create_if_not_sender_skips_self_notification(self):
        result = NotificationService.create_if_not_sender(
            recipient=self.user1,
            sender=self.user1,
            notification_type='test',
            message='test',
        )

        self.assertIsNone(result)
        self.assertEqual(Notification.objects.count(), 0)

    def test_notify_like_artwork_creates_notification(self):
        NotificationService.notify_like(self.artwork, self.user2)
        notification = Notification.objects.first()
        self.assertEqual(notification.recipient, self.user1)

    def test_notify_like_artwork_not_when_owner(self):
        NotificationService.notify_like(self.artwork, self.user1)
        self.assertEqual(Notification.objects.count(), 0)

    def test_notify_like_comment(self):
        comment = Comment.objects.create(
            user=self.user1,
            artwork =self.artwork,
            content='test'
        )

        NotificationService.notify_like(comment, self.user2)
        notification = Notification.objects.first()
        self.assertEqual(notification.recipient, self.user1)

    def test_notify_comment_on_artwork(self):
        comment = Comment.objects.create(
            user=self.user2,
            artwork =self.artwork,
            content='test'
        )

        NotificationService.notify_comment(comment)
        notification = Notification.objects.first()
        self.assertEqual(notification.recipient, self.user1)

    def test_notify_comment_reply(self):
        parent = Comment.objects.create(
            user=self.user1,
            artwork=self.artwork,
            content='test'
        )

        reply = Comment.objects.create(
            user=self.user2,
            artwork=self.artwork,
            parent=parent,
            content='test'
        )

        NotificationService.notify_comment(reply)
        notification = Notification.objects.first()
        self.assertEqual(notification.recipient, self.user1)

    def test_notify_new_post(self):
        GroupMember.objects.create(
            group=self.group,
            user=self.user2,
            role=RoleChoices.MEMBER
        )

        post = Post.objects.create(
            group=self.group,
            author=self.user1,
            content='test'
        )

        NotificationService.notify_new_post(post)
        self.assertEqual(Notification.objects.count(), 1)

    def test_notify_submission_only_admins(self):
        GroupMember.objects.create(
            group=self.group,
            user=self.user2,
            role=RoleChoices.ADMIN
        )

        NotificationService.notify_submission(
            sender=self.user3,
            group=self.group,
            artwork=self.artwork,
        )

        notification = Notification.objects.first()
        self.assertEqual(notification.recipient, self.user2)

    def test_notify_join_request(self):
        NotificationService.notify_join_request(self.user2, self.group)
        notification = Notification.objects.first()
        self.assertEqual(notification.recipient, self.group.owner)