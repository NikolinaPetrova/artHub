from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from notifications.choices import NotificationsChoices
from notifications.models import Notification

UserModel = get_user_model()


class NotificationListViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = UserModel.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='123pass123'
        )

        self.other_user = UserModel.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='123pass123'
        )

        self.url = reverse('notification-list')

    def test_requires_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_returns_only_unread_notifications_for_user(self):
        Notification.objects.create(
            recipient=self.user,
            sender=self.other_user,
            notification_type=NotificationsChoices.COMMENT_ARTWORK,
            message='unread notification'
        )

        Notification.objects.create(
            recipient=self.user,
            sender=self.other_user,
            notification_type=NotificationsChoices.COMMENT_ARTWORK,
            message='read notification',
            is_read=True,
        )

        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['message'], 'unread notification')

    def test_does_not_return_notifications_for_other_users(self):
        Notification.objects.create(
            recipient=self.other_user,
            sender=self.user,
            notification_type=NotificationsChoices.COMMENT_ARTWORK,
            message='other user notification'
        )

        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(len(response.data), 0)

    def test_returns_max_20_notifications(self):
        for i in range(25):
            Notification.objects.create(
                recipient=self.user,
                sender=self.other_user,
                notification_type=NotificationsChoices.COMMENT_ARTWORK,
                message=f'Notification {i}'
            )

        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(len(response.data), 20)
