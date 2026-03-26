from django.contrib.auth.models import Permission
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from artworks.choices import ArtworkTypeChoices
from artworks.models import Artwork

UserModel = get_user_model()

class EditArtworkViewTest(TestCase):
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

        self.editor = UserModel.objects.create_user(
            username='editor',
            email='editor@test.com',
            password='123pass123'
        )

        self.artwork = Artwork.objects.create(
            title='Test title',
            description='Test description',
            image_url='https://example.com/test.jpg',
            type=ArtworkTypeChoices.PHOTOGRAPHY,
            user=self.owner,
        )

    def test_owner_can_access_edit_view(self):
        self.client.login(username='owner', password='123pass123')
        response = self.client.get(
            reverse('edit-artwork', kwargs={'pk': self.artwork.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_non_owner_gets_404(self):
        self.client.login(username='other', password='123pass123')

        response = self.client.get(
            reverse('edit-artwork', kwargs={'pk': self.artwork.pk})
        )

        self.assertEqual(response.status_code, 404)

    def test_user_with_permission_can_access_edit_view(self):
        permission = Permission.objects.get(codename='change_artwork')
        self.editor.user_permissions.add(permission)
        self.client.login(username='editor', password='123pass123')

        response = self.client.get(
            reverse('edit-artwork', kwargs={'pk': self.artwork.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_owner_can_edit(self):
        self.client.login(username='owner', password='123pass123')

        response = self.client.post(
            reverse('edit-artwork', kwargs={'pk': self.artwork.pk}),
            data={
                'title': 'Updated title',
                'description': self.artwork.description,
                'image_url': self.artwork.image_url,
                'type': self.artwork.type,
                'tags': '',
            }
        )

        self.artwork.refresh_from_db()

        self.assertRedirects(
            response,
            reverse('artwork-details', kwargs={'pk': self.artwork.pk})
        )
        self.assertEqual(self.artwork.title, 'Updated title')