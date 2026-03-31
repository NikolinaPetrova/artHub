from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Permission
from artworks.choices import ArtworkTypeChoices
from artworks.models import Artwork
from groups.models import Group, Post
from interactions.models import Comment

UserModel = get_user_model()

class CommentEditViewTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='123pass123',
        )
        self.other_user = UserModel.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='123pass123',
        )

        self.artwork = Artwork.objects.create(
            title='Test artwork',
            description='desc',
            image_url='https://example.com/image.jpg',
            type=ArtworkTypeChoices.PAINTING,
            user=self.user,
        )

        self.group = Group.objects.create(
            name='Test Group',
            slug='test-group',
            owner=self.user,
        )

        self.post = Post.objects.create(
            group=self.group,
            author=self.user,
            content='Test post content',
        )

        self.artwork_comment = Comment.objects.create(
            content='Old artwork comment',
            user=self.user,
            artwork=self.artwork,
        )

        self.post_comment = Comment.objects.create(
            content='Old post comment',
            user=self.user,
            post=self.post,
        )

    def test_owner_can_edit_comment(self):
        self.client.login(username='user1', password='123pass123')
        response = self.client.post(
            reverse('edit-comment', kwargs={'pk': self.artwork_comment.pk}),
            data={'content': 'Updated artwork comment'},
        )

        self.artwork_comment.refresh_from_db()
        self.assertEqual(self.artwork_comment.content, 'Updated artwork comment')
        self.assertRedirects(
            response,
            reverse('artwork-details', kwargs={'pk': self.artwork.pk})
        )

    def test_user_with_permission_can_edit_comment(self):
        permission = Permission.objects.get(codename='change_comment')
        self.other_user.user_permissions.add(permission)
        self.client.login(username='user2', password='123pass123')
        response = self.client.post(
            reverse('edit-comment', kwargs={'pk': self.artwork_comment.pk}),
            data={'content': 'Edited by permitted user'},
        )

        self.artwork_comment.refresh_from_db()
        self.assertEqual(self.artwork_comment.content, 'Edited by permitted user')
        self.assertRedirects(
            response,
            reverse('artwork-details', kwargs={'pk': self.artwork.pk})
        )

    def test_user_without_permission_cannot_edit_comment(self):
        self.client.login(username='user2', password='123pass123')
        response = self.client.post(
            reverse('edit-comment', kwargs={'pk': self.artwork_comment.pk}),
            data={'content': 'Unauthorized edit'},
        )

        self.artwork_comment.refresh_from_db()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.artwork_comment.content, 'Old artwork comment')
        self.assertIn('You cannot edit this comment.', response.content.decode())

    def test_invalid_form_does_not_update_comment(self):
        self.client.login(username='user1', password='123pass123')
        response = self.client.post(
            reverse('edit-comment', kwargs={'pk': self.artwork_comment.pk}),
            data={'content': ' '},
        )

        self.artwork_comment.refresh_from_db()
        self.assertEqual(self.artwork_comment.content, 'Old artwork comment')
        self.assertRedirects(
            response,
            reverse('artwork-details', kwargs={'pk': self.artwork.pk})
        )

    def test_redirects_to_post_details_when_comment_is_for_post(self):
        self.client.login(username='user1', password='123pass123')
        response = self.client.post(
            reverse('edit-comment', kwargs={'pk': self.post_comment.pk}),
            data={'content': 'Updated post comment'},
        )

        self.post_comment.refresh_from_db()
        self.assertEqual(self.post_comment.content, 'Updated post comment')
        self.assertRedirects(
            response,
            reverse('post-details', kwargs={'slug': self.group.slug, 'pk': self.post.pk})
        )

    def test_redirects_to_home_when_comment_has_no_artwork_or_post(self):
        orphan_comment = Comment.objects.create(
            content='Standalone comment',
            user=self.user,
        )
        self.client.login(username='user1', password='123pass123')

        response = self.client.post(
            reverse('edit-comment', kwargs={'pk': orphan_comment.pk}),
            data={'content': 'Updated standalone comment'},
        )

        orphan_comment.refresh_from_db()
        self.assertEqual(orphan_comment.content, 'Updated standalone comment')
        self.assertRedirects(response, reverse('home'))