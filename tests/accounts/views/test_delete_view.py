from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

UserModel = get_user_model()

class UserDeleteViewTests(TestCase):
    def setUp(self):
        self.user1 = UserModel.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='123pass123',
        )
        self.user2 = UserModel.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='123pass123',
        )

    @patch('accounts.views.can_manage_user', return_value=False)
    def test_user_without_permission_is_redirected_to_home(self, mock_can_manage_user):
        self.client.login(username='user1', password='123pass123')

        response = self.client.get(
            reverse('delete-profile', kwargs={'pk': self.user2.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

    @patch('accounts.views.can_manage_user', return_value=True)
    def test_confirm_yes_deletes_user(self, mock_can_manage_user):
        self.client.login(username='user1', password='123pass123')

        response = self.client.post(
            reverse('delete-profile', kwargs={'pk': self.user2.pk}),
            data={'confirm': 'yes'}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))
        self.assertFalse(UserModel.objects.filter(pk=self.user2.pk).exists())

    @patch('accounts.views.can_manage_user', return_value=True)
    def test_confirm_no_does_not_delete_user(self, mock_can_manage_user):
        self.client.login(username='user1', password='123pass123')

        response = self.client.post(
            reverse('delete-profile', kwargs={'pk': self.user2.pk}),
            data={'confirm': 'no'}
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse('profile-details', kwargs={'pk': self.user2.pk})
        )
        self.assertTrue(UserModel.objects.filter(pk=self.user2.pk).exists())