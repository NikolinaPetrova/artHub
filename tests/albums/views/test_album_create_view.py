from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from albums.models import Album

UserModel = get_user_model()

class AlbumCreateViewTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='123pass123'
        )

        self.url = reverse('album-create')

    def test_redirects_anonymous_user_to_login(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_get_request_adds_album_form_to_context(self):
        self.client.login(username='user1', password='123pass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('album_form', response.context)

    def test_form_valid_sets_request_user_as_owner(self):
        self.client.login(username='user1', password='123pass123')

        response = self.client.post(self.url, data={
            'name': 'Album'
        })

        self.assertEqual(response.status_code, 302)
        album = Album.objects.get(name='Album')
        self.assertEqual(album.owner, self.user)

    def test_successful_create_redirects_to_profile_details(self):
        self.client.login(username='user1', password='123pass123')
        response = self.client.post(self.url, data={
            'name': 'Album'
        })

        self.assertRedirects(response, reverse('profile-details', kwargs={'pk': self.user.pk}))