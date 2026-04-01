from django.contrib.auth import get_user_model
from django.test import TestCase
from notifications.choices import NotificationsChoices
from notifications.models import Notification
from notifications.serializers import NotificationSerializer

UserModel = get_user_model()

class NotificationSerializerTests(TestCase):
    def setUp(self):
        self.sender = UserModel.objects.create_user(
            username='sender',
            email='sender@test.com',
            password='123pass123'
        )

        self.recipient = UserModel.objects.create_user(
            username='recipient',
            email='recipient@test.com',
            password='123pass123'
        )

        self.notification = Notification.objects.create(
            recipient=self.recipient,
            sender=self.sender,
            notification_type=NotificationsChoices.COMMENT_ARTWORK,
            message='Test notification'
        )

    def test_serializer_returns_sender_username(self):
        serializer = NotificationSerializer(self.notification)
        self.assertEqual(
            serializer.data['sender_username'],
            self.sender.username
        )

    def test_serializer_returns_non_when_sender_has_no_avatar(self):
        serializer = NotificationSerializer(self.notification)
        self.assertIsNone(serializer.data['sender_avatar'])

    def test_serializer_returns_sender_avatar_when_exists(self):
        self.sender.profile.avatar = 'https://example.com/avatar.jpg'
        self.sender.profile.save()

        serializer = NotificationSerializer(self.notification)
        self.assertTrue(serializer.data['sender_avatar'])