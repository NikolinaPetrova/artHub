from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from notifications.choices import NotificationsChoices
from notifications.models import Notification

UserModel = get_user_model()

class MarkNotificationReadViewTests(TestCase):

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

        self.notification = Notification.objects.create(
            recipient=self.user,
            sender=self.other_user,
            notification_type=NotificationsChoices.COMMENT_ARTWORK,
            message='unread notification',
            is_read=False
        )

        self.other_notification = Notification.objects.create(
            recipient=self.other_user,
            sender=self.user,
            notification_type=NotificationsChoices.COMMENT_ARTWORK,
            message='other user notification',
            is_read=False
        )

    def test_requires_authentication(self):
        url = reverse('notification-read', kwargs={'pk': self.notification.pk})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_marks_own_notification_as_read(self):
        url = reverse('notification-read', kwargs={'pk': self.notification.pk})
        self.client.force_authenticate(self.user)
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)

    def test_user_cannot_mark_other_users_notification_as_read(self):
        url = reverse('notification-read', kwargs={'pk': self.other_notification.pk})
        self.client.force_authenticate(self.user)
        response = self.client.patch(url, {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.other_notification.refresh_from_db()
        self.assertFalse(self.other_notification.is_read)