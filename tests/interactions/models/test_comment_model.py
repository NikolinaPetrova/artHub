from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from artworks.choices import ArtworkTypeChoices
from artworks.models import Artwork
from interactions.models import Comment

UserModel = get_user_model()

class CommentModelTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username="test",
            email="test@test.com",
            password="123pass123"
        )

        self.artwork = Artwork.objects.create(
            title='Test title',
            description='Test description',
            image_url='https://example.com/test.jpg',
            type=ArtworkTypeChoices.PAINTING,
            user=self.user,
        )

    def test_content_min_length_validator_raises_error_for_short_content(self):
        comment = Comment(
            content='A',
            user=self.user,
            artwork=self.artwork,
        )

        with self.assertRaises(ValidationError):
            comment.full_clean()

    def test_top_level_returns_self_when_comment_has_no_parent(self):
        comment = Comment.objects.create(
            content='top level comment',
            user=self.user,
            artwork=self.artwork,
        )

        self.assertEqual(comment.top_level, comment)

    def test_top_level_returns_root_parent_for_nested_reply(self):
        top_level_comment = Comment.objects.create(
            content='top level comment',
            user=self.user,
            artwork=self.artwork,
        )

        child = Comment.objects.create(
            content='child comment',
            user=self.user,
            artwork=self.artwork,
            parent=top_level_comment,
        )

        nested_reply = Comment.objects.create(
            content='nested reply',
            user=self.user,
            artwork=self.artwork,
            parent=child,
        )

        self.assertEqual(child.top_level, top_level_comment)
        self.assertEqual(nested_reply.top_level, top_level_comment)

    def test_str_returns_expected_value(self):
        comment = Comment.objects.create(
            content='test',
            user=self.user,
            artwork=self.artwork,
        )

        self.assertEqual(str(comment), 'Comment by test')
