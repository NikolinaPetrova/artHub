from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

UserModel = get_user_model()

class UserUpdateViewTests(TestCase):
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

    def test_user_can_open_own_edit_page(self):
        self.client.login(username='user1', password='123pass123')
        response = self.client.get(
            reverse('edit-profile', kwargs={'pk': self.user1.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_user_cannot_open_other_user_edit_page(self):
        self.client.login(username='user1', password='123pass123')
        response = self.client.get(
            reverse('edit-profile', kwargs={'pk': self.user2.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse('profile-details', kwargs={'pk': self.user1.pk})
        )

    def test_successful_update_redirects_to_own_profile(self):
        self.client.login(username='user1', password='123pass123')
        response = self.client.post(
            reverse('edit-profile', kwargs={'pk': self.user1.pk}),
            data={
                'first_name': 'Test',
                'last_name': 'User',
                'email': 'newemail@test.com',
                'description': '',
                'professional_artist': False,
            }
        )

        self.user1.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse('profile-details', kwargs={'pk': self.user1.pk})
        )
        self.assertEqual(self.user1.email, 'newemail@test.com')