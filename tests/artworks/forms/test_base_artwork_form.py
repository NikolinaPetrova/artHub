from django.contrib.auth import get_user_model
from django.test import TestCase
from albums.models import Album
from artworks.choices import ArtworkTypeChoices
from artworks.forms import BaseArtworkForm
from artworks.models import Tag, Artwork

UserModel = get_user_model()


class BaseArtworkFormTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='123pass123'
        )

    def test_clean_tags_returns_cleaned_list(self):
        form = BaseArtworkForm(
            data={
                'title': 'Test artwork',
                'description': 'test',
                'image_url': 'https://example.com/image.jpg',
                'type': ArtworkTypeChoices.PHOTOGRAPHY,
                'tags': '   Art,   test-tag, art, demo   '
            },
            user=self.user
        )

        self.assertTrue(form.is_valid())
        cleaned_tags = form.cleaned_data['tags']
        self.assertIn('art', cleaned_tags)
        self.assertIn('test-tag', cleaned_tags)
        self.assertIn('demo', cleaned_tags)

    def test_clean_tags_raises_error_for_invalid_tag(self):
        form = BaseArtworkForm(
            data={
                'title': 'Test artwork',
                'description': 'test',
                'image_url': 'https://example.com/image.jpg',
                'type': ArtworkTypeChoices.PHOTOGRAPHY,
                'tags': 'valid-tag, invalid@tag',
            },
            user=self.user
        )

        self.assertFalse(form.is_valid())
        self.assertIn('tags', form.errors)
        self.assertIn('Invalid tag: "invalid@tag"', form.errors['tags'])

    def test_save_creates_artwork_and_tags(self):
        form = BaseArtworkForm(
            data={
                'title': 'Test artwork',
                'description': 'test',
                'image_url': 'https://example.com/image.jpg',
                'type': ArtworkTypeChoices.PHOTOGRAPHY,
                'tags': 'art, test-tag',
            },
            user=self.user
        )

        self.assertTrue(form.is_valid())
        artwork = form.save()
        self.assertEqual(artwork.user, self.user)
        self.assertEqual(artwork.title, 'Test artwork')
        self.assertEqual(artwork.tags.count(), 2)
        self.assertTrue(Tag.objects.filter(name='art').exists())
        self.assertTrue(Tag.objects.filter(name='test-tag').exists())

    def test_albums_queryset_contains_only_user_albums(self):
        other_user = UserModel.objects.create_user(
            username='otheruser',
            email='otheruser@test.com',
            password='123pass123'
        )

        user_album = Album.objects.create(
            name='Test Album',
            owner=self.user,
        )

        other_album = Album.objects.create(name='Other Album', owner=other_user)

        form = BaseArtworkForm(user=self.user)
        queryset = form.fields['albums'].queryset

        self.assertIn(user_album, queryset)
        self.assertNotIn(other_album, queryset)

    def test_form_sets_initial_tags_when_editing_artwork(self):
        artwork = Artwork.objects.create(
            title='Test Artwork',
            description='test',
            image_url='https://example.com/image.jpg',
            type=ArtworkTypeChoices.PHOTOGRAPHY,
            user=self.user,
        )

        tag1 = Tag.objects.create(name='art')
        tag2 = Tag.objects.create(name='test-tag')

        artwork.tags.add(tag1, tag2)
        form = BaseArtworkForm(instance=artwork, user=self.user)

        self.assertIn('art', form.initial['tags'])
        self.assertIn('test-tag', form.initial['tags'])
