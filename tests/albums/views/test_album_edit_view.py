from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from albums.models import Album
from artworks.models import Artwork

UserModel = get_user_model()

class AlbumEditViewTests(TestCase):
    def setUp(self):
        self.owner = UserModel.objects.create_user(
            username='owner',
            email='owner@exmaple.com',
            password='123pass123',
        )

        self.other_user = UserModel.objects.create_user(
            username='other',
            email='other@example.com',
            password='123pass123',
        )

        self.album = Album.objects.create(
            name = 'Album',
            owner = self.owner,
        )

        self.artwork = Artwork.objects.create(
            title = 'Test artwork',
            image_url = 'https://example.com/artwork.jpg',
            user=self.owner,
        )

        self.album.artworks.add(self.artwork)
        self.url = reverse('edit-album', kwargs={'pk': self.album.pk})

    def test_redirects_anonymous_user_to_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_owner_can_access_edit_view(self):
        self.client.login(username='owner', password='123pass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_non_owner_without_permission_cannot_access(self):
        self.client.login(username='other', password='123pass123')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_user_with_permission_can_access(self):
        permission = Permission.objects.get(codename='change_album')
        self.other_user.user_permissions.add(permission)
        self.client.login(username='other', password='123pass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_with_remove_artwork_removes_artwork_from_album(self):
        self.client.login(username='owner', password='123pass123')
        response = self.client.post(self.url, data={
            'remove_artwork': self.artwork.pk
        })
        self.assertRedirects(response, self.url)
        self.assertNotIn(self.artwork, self.album.artworks.all())

    def test_successful_edit_redirects_to_profile_details(self):
        self.client.login(username='owner', password='123pass123')
        response = self.client.post(self.url, data={
            'name': 'Updated Album name'
        })

        self.album.refresh_from_db()
        self.assertEqual(self.album.name, 'Updated Album name')
        self.assertRedirects(
            response,
            reverse('profile-details', kwargs={'pk': self.owner.pk})
        )