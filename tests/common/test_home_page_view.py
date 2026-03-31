from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from artworks.choices import ArtworkTypeChoices
from artworks.models import Artwork
from interactions.models import Like


UserModel = get_user_model()


class HomePageViewTests(TestCase):
    def setUp(self):
        self.author = UserModel.objects.create_user(
            username='author',
            email='author@test.com',
            password='123pass123',
        )

        self.user1 = UserModel.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='123pass123',
        )
        self.user2 = UserModel.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='123pass123',
        )
        self.user3 = UserModel.objects.create_user(
            username='user3',
            email='user3@test.com',
            password='123pass123',
        )
        self.user4 = UserModel.objects.create_user(
            username='user4',
            email='user4@test.com',
            password='123pass123',
        )
        self.user5 = UserModel.objects.create_user(
            username='user5',
            email='user5@test.com',
            password='123pass123',
        )
        self.user6 = UserModel.objects.create_user(
            username='user6',
            email='user6@test.com',
            password='123pass123',
        )

        self.artwork1 = Artwork.objects.create(
            title='Artwork 1',
            image_url='https://example.com/1.jpg',
            type=ArtworkTypeChoices.PAINTING,
            user=self.author,
        )
        self.artwork2 = Artwork.objects.create(
            title='Artwork 2',
            image_url='https://example.com/2.jpg',
            type=ArtworkTypeChoices.PAINTING,
            user=self.author,
        )
        self.artwork3 = Artwork.objects.create(
            title='Artwork 3',
            image_url='https://example.com/3.jpg',
            type=ArtworkTypeChoices.PAINTING,
            user=self.author,
        )
        self.artwork4 = Artwork.objects.create(
            title='Artwork 4',
            image_url='https://example.com/4.jpg',
            type=ArtworkTypeChoices.PAINTING,
            user=self.author,
        )
        self.artwork5 = Artwork.objects.create(
            title='Artwork 5',
            image_url='https://example.com/5.jpg',
            type=ArtworkTypeChoices.PAINTING,
            user=self.author,
        )
        self.artwork6 = Artwork.objects.create(
            title='Artwork 6',
            image_url='https://example.com/6.jpg',
            type=ArtworkTypeChoices.PAINTING,
            user=self.author,
        )

        Like.objects.create(user=self.user1, artwork=self.artwork1)
        Like.objects.create(user=self.user2, artwork=self.artwork1)
        Like.objects.create(user=self.user3, artwork=self.artwork1)
        Like.objects.create(user=self.user1, artwork=self.artwork2)
        Like.objects.create(user=self.user2, artwork=self.artwork2)
        Like.objects.create(user=self.user1, artwork=self.artwork3)
        Like.objects.create(user=self.user1, artwork=self.artwork4)
        Like.objects.create(user=self.user2, artwork=self.artwork4)
        Like.objects.create(user=self.user3, artwork=self.artwork4)
        Like.objects.create(user=self.user4, artwork=self.artwork4)
        Like.objects.create(user=self.user1, artwork=self.artwork5)
        Like.objects.create(user=self.user2, artwork=self.artwork5)
        Like.objects.create(user=self.user3, artwork=self.artwork5)
        Like.objects.create(user=self.user4, artwork=self.artwork5)
        Like.objects.create(user=self.user5, artwork=self.artwork5)
        Like.objects.create(user=self.user1, artwork=self.artwork6)
        Like.objects.create(user=self.user2, artwork=self.artwork6)
        Like.objects.create(user=self.user3, artwork=self.artwork6)
        Like.objects.create(user=self.user4, artwork=self.artwork6)
        Like.objects.create(user=self.user5, artwork=self.artwork6)
        Like.objects.create(user=self.user6, artwork=self.artwork6)

        self.url = reverse('home')

    def test_adds_top_artworks_to_context(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn('top_artworks', response.context)

    def test_top_artworks_are_ordered_by_likes_count_desc(self):
        response = self.client.get(self.url)

        top_artworks = list(response.context['top_artworks'])

        self.assertEqual(
            top_artworks,
            [
                self.artwork6,
                self.artwork5,
                self.artwork4,
                self.artwork1,
                self.artwork2,
            ]
        )

    def test_top_artworks_are_limited_to_five(self):
        response = self.client.get(self.url)

        top_artworks = list(response.context['top_artworks'])

        self.assertEqual(len(top_artworks), 5)