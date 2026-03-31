from django.test import TestCase
from interactions.forms import BaseCommentForm


class BaseCommentFormTests(TestCase):
    def test_clean_content_strips_whitespace(self):
        form = BaseCommentForm(
            data={'content': '   comment    '}
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['content'], 'comment')

    def test_comment_with_only_spaces_is_invalid(self):
        form = BaseCommentForm(data={
            'content': '        '
        })

        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)