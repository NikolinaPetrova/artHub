from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from artworks.models import Tag, Artwork

UserModel = get_user_model()

class GalleryPageViewTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='123pass123',
        )

        self.tag_nature, _ = Tag.objects.get_or_create(name='nature')
        self.tag_digital, _ = Tag.objects.get_or_create(name='digital')

        self.artwork1 = Artwork.objects.create(
            title='Unique Nature Artwork',
            image_url='https://example.com/artwork.jpg',
            user=self.user,
        )
        self.artwork1.tags.add(self.tag_nature)

        self.artwork2 = Artwork.objects.create(
            title='Unique Digital Artwork',
            image_url='https://example.com/artwork2.jpg',
            user=self.user,
        )
        self.artwork2.tags.add(self.tag_digital)

        self.url = reverse('gallery')

    def test_filters_artworks_by_title(self):
        response = self.client.get(self.url, {'q': 'Unique Digital'})

        self.assertEqual(response.status_code, 200)
        artworks = response.context['artwork_list']

        self.assertIn(self.artwork2, artworks)

    def test_filters_artworks_by_tag_name(self):
        response = self.client.get(self.url, {'q': 'nature'})

        self.assertEqual(response.status_code, 200)
        artworks = response.context['artwork_list']

        self.assertIn(self.artwork1, artworks)

    def test_query_is_split_into_words_and_matches_any_word(self):
        response = self.client.get(self.url, {'q': 'nature digital'})

        self.assertEqual(response.status_code, 200)
        artworks = response.context['artwork_list']

        self.assertIn(self.artwork1, artworks)
        self.assertIn(self.artwork2, artworks)

    def test_adds_tags_to_context(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertIn('tags', response.context)

    def test_ajax_request_returns_json_response(self):
        response = self.client.get(
            self.url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        data = response.json()

        self.assertIn('html', data)
        self.assertIn('has_next', data)
        self.assertIn('next_page_number', data)