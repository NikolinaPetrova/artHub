from django.contrib.auth import get_user_model
from django.test import TestCase
from groups.forms.post import BasePostForm

UserModel = get_user_model()

class BasePostFormTests(TestCase):
    def test_clean_title_strips_whitespace(self):
        form = BasePostForm(
            data={
                'title': '    test title   ',
                'content': 'test content',
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['title'], 'test title')

    def test_clean_title_raises_error_when_title_is_less_than_3_chars(self):
        form = BasePostForm(
            data={
                'title': '    ab   ',
                'content': 'ab content',
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('Title must be at least 3 characters long', form.errors['title'])

    def test_clean_content_strips_whitespace(self):
        form = BasePostForm(
            data={
                'title': 'test title',
                'content': '     test content    ',
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['content'], 'test content')

    def test_clean_content_raises_error_when_content_is_only_whitespace(self):
        form = BasePostForm(
            data={
                'title': 'test title',
                'content': '     ',
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)
        self.assertIn('Content cannot be empty', form.errors['content'])