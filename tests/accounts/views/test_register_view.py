from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

UserModel = get_user_model()

class RegisterViewTests(TestCase):

    def setUp(self):
        self.url = reverse('register')
        self.valid_data = {
            'username': 'test123',
            'email': 'test@test.com',
            'password1': '123pass123',
            'password2': '123pass123',
        }

    def test_logged_in_user_is_redirected_from_register_page(self):
        UserModel.objects.create_user(
            username=self.valid_data['username'],
            email=self.valid_data['email'],
            password=self.valid_data['password1'],
        )
        self.client.login(username='test123', password='123pass123')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))

    @patch('accounts.views.send_welcome_email.delay')
    def test_valid_register_logs_in_user(self, mock_send_welcome_email):
        response = self.client.post(self.url, data=self.valid_data)

        created_user = UserModel.objects.get(username='test123')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))
        self.assertEqual(int(self.client.session['_auth_user_id']), created_user.pk)

    @patch('accounts.views.send_welcome_email.delay')
    def test_valid_register_sends_welcome_email(self, mock_send_welcome_email):
        self.client.post(self.url, data=self.valid_data)

        created_user = UserModel.objects.get(username='test123')

        mock_send_welcome_email.assert_called_once_with(
            created_user.email,
            created_user.username,
        )

    @patch('accounts.views.send_welcome_email.delay')
    def test_invalid_register_does_not_create_user(self, mock_send_welcome_email):
        response = self.client.post(self.url, data={
            'username': 'invaliduser',
            'email': 'invaliduser@test.com',
            'password1': '123pass123',
            'password2': '123diffpass123',
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(UserModel.objects.filter(username='invaliduser').exists())
        mock_send_welcome_email.assert_not_called()