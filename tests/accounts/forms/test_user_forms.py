from django.contrib.auth import get_user_model
from django.test import TestCase
from accounts.forms import ArtHubUserCreationForm

UserModel = get_user_model()

class UserFormsTests(TestCase):
    def test_valid_username_passes(self):
        form = ArtHubUserCreationForm(data={
            'username': 'valid_user123',
            'email': 'test@test.com',
            'password1': '123pass123',
            'password2': '123pass123',
        })

        self.assertTrue(form.is_valid())

    def test_invalid_username_raises_error(self):
        form = ArtHubUserCreationForm(data={
            'username': 'INVALID_USER!',
            'email': 'test@test.com',
            'password1': '123pass123',
            'password2': '123pass123',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)

    def test_username_cannot_start_with_dash(self):
        form = ArtHubUserCreationForm(data={
            'username': '-user',
            'email': 'test@test.com',
            'password1': '123pass123',
            'password2': '123pass123',
        })

        self.assertFalse(form.is_valid())

    def test_username_cannot_start_with_underscore(self):
        form = ArtHubUserCreationForm(data={
            'username': '_user',
            'email': 'test@test.com',
            'password1': '123pass123',
            'password2': '123pass123',
        })

        self.assertFalse(form.is_valid())

    def test_email_already_exists(self):
        UserModel.objects.create_user(
            username='valid_user123',
            email='test@test.com',
            password='123pass123',
        )


        form = ArtHubUserCreationForm(data={
            'username': 'user123',
            'email': 'test@test.com',
            'password1': '123pass123',
            'password2': '123pass123',
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['email'][0],
            'User with this email already exists.'
        )