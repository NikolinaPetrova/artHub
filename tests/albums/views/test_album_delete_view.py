from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from albums.models import Album

UserModel = get_user_model()


class AlbumDeleteViewTests(TestCase):
    def setUp(self):
        self.owner = UserModel.objects.create_user(
            username='owner',
            email='owner@test.com',
            password='123pass123'
        )

        self.other_user = UserModel.objects.create_user(
            username='other',
            email='other@test.com',
            password='123pass123'
        )

        self.album = Album.objects.create(
            name='Album',
            owner=self.owner,
        )

        self.url = reverse('album-delete', kwargs={'pk': self.album.pk})

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test_owner_can_delete_album(self):
        self.client.login(username='owner', password='123pass123')
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            reverse('profile-details', kwargs={'pk': self.owner.pk})
        )
        self.assertFalse(Album.objects.filter(pk=self.album.pk).exists())

    def test_non_owner_without_permission_gets_404(self):
        self.client.login(username='other', password='123pass123')
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Album.objects.filter(pk=self.album.pk).exists())

    def test_user_with_permission_can_delete_album(self):
        permission = Permission.objects.get(codename='delete_album')
        self.other_user.user_permissions.add(permission)
        self.client.login(username='other', password='123pass123')
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            reverse('profile-details', kwargs={'pk': self.owner.pk})
        )

        self.assertFalse(Album.objects.filter(pk=self.album.pk).exists())
