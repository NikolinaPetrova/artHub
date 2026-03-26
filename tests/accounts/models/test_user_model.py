from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

UserModel = get_user_model()

class ArtHubUserModelTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser123',
            email='testuser123@example.com',
            password='123pass123',
            first_name='   tEst   ',
            last_name='   uSeR   '
        )

    def test_save_strips_and_capitalizes_first_name(self):
        self.assertEqual(self.user.first_name,'Test')

    def test_save_strips_and_capitalizes_last_name(self):
        self.assertEqual(self.user.last_name,'User')

    def test_save_strips_and_capitalizes_first_and_last_name(self):
        self.assertEqual(self.user.first_name,'Test')
        self.assertEqual(self.user.last_name,'User')

    def test_str_returns_username(self):
        self.assertEqual(str(self.user), 'testuser123')

    def test_second_user_with_same_email_raise_exception(self):
        with self.assertRaises(IntegrityError):
            UserModel.objects.create_user(
                username='testuser900',
                email='testuser123@example.com',
                password='123pass123',
            )
