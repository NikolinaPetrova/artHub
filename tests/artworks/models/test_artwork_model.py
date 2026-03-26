from django.contrib.auth import get_user_model
from django.test import TestCase
from artworks.choices import ArtworkTypeChoices
from artworks.models import Artwork

UserModel = get_user_model()

class ArtworkModelTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='123pass123',
        )

    def test_str_returns_title(self):
        artwork = Artwork.objects.create(
            title='Test Art',
            image_url='https://example.com/test.jpg',
            type=ArtworkTypeChoices.PAINTING,
            user=self.user
        )

        self.assertEqual(str(artwork), 'Test Art')

