from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse
from artworks.choices import ArtworkTypeChoices
from artworks.models import Artwork

UserModel = get_user_model()

class DeleteArtworkViewTest(TestCase):
    def setUp(self):
        self.owner = UserModel.objects.create_user(
            username="owner",
            email="owner@test.com",
            password="123pass123"
        )

        self.other_user = UserModel.objects.create_user(
            username="other",
            email="other@test.com",
            password="123pass123"
        )

        self.moderator = UserModel.objects.create_user(
            username="moderator",
            email="moderator@test.com",
            password="123pass123"
        )

        self.artwork = Artwork.objects.create(
            title='Test artwork',
            description='Test description',
            image_url = 'https://example.com/artwork.jpg',
            type=ArtworkTypeChoices.PHOTOGRAPHY,
            user=self.owner,
        )
    def test_owner_can_access_delete_view(self):
        self.client.login(username="owner", password="123pass123")
        response = self.client.get(
            reverse('delete-artwork', kwargs={'pk': self.artwork.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_user_with_permission_can_access_delete_view(self):
        permission = Permission.objects.get(codename='delete_artwork')
        self.moderator.user_permissions.add(permission)
        self.client.login(username='moderator', password='123pass123')

        response = self.client.get(
            reverse('delete-artwork', kwargs={'pk': self.artwork.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_non_owner_without_permission_gets_404(self):
        self.client.login(username='other', password='123pass123')

        response = self.client.get(
            reverse('delete-artwork', kwargs={'pk': self.artwork.pk})
        )

        self.assertEqual(response.status_code, 404)

    def test_confirm_yes_deletes_artwork_and_redirects_to_gallery(self):
        self.client.login(username='owner', password='123pass123')

        response = self.client.post(
            reverse('delete-artwork', kwargs={'pk': self.artwork.pk}),
            data={'confirm': 'yes'},
        )

        self.assertRedirects(response, reverse('gallery'))
        self.assertFalse(Artwork.objects.filter(pk=self.artwork.pk).exists())

    def test_confirm_no_does_not_delete_artwork_and_redirects_to_details(self):
        self.client.login(username='owner', password='123pass123')

        response = self.client.post(
            reverse('delete-artwork', kwargs={'pk': self.artwork.pk}),
            data={'confirm': 'no'},
        )

        self.assertRedirects(
            response,
            reverse('artwork-details', kwargs={'pk': self.artwork.pk})
        )
        self.assertTrue(Artwork.objects.filter(pk=self.artwork.pk).exists())