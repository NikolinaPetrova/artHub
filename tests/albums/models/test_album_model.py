from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from albums.models import Album

UserModel = get_user_model()

class AlbumModelTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='123pass123',
        )

        self.user2 = UserModel.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='123pass123',
        )
    def test_str_returns_album_name(self):
        album = Album.objects.create(
            name='Album',
            owner=self.user,
        )

        self.assertEqual(str(album), 'Album')

    def test_name_min_length_validator(self):
        album = Album(name='ab', owner=self.user)

        with self.assertRaises(ValidationError) as e:
            album.full_clean()

        self.assertIn('name', e.exception.message_dict)

    def test_album_name_unique_per_owner(self):
        Album.objects.create(
            name='Album',
            owner=self.user,
        )

        album = Album(
            name='Album',
            owner=self.user,
        )

        with self.assertRaises(ValidationError):
            album.full_clean()

    def test_different_users_can_have_same_album_name(self):
        Album.objects.create(
            name='Album',
            owner=self.user,
        )

        album = Album(
            name='Album',
            owner=self.user2,
        )

        album.full_clean()


