from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from artworks.models import Artwork
from artworks.choices import ArtworkTypeChoices
from groups.models import Group, GroupFolder, GroupMember
from groups.choices import JoinPolicy, RoleChoices

UserModel = get_user_model()


class GroupFolderEditViewTests(TestCase):

    def setUp(self):
        self.owner = UserModel.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='123pass123',
        )
        self.other_user = UserModel.objects.create_user(
            username='other',
            email='other@example.com',
            password='123pass123',
        )

        self.group = Group.objects.create(
            name='Group One',
            description='Test group',
            owner=self.owner,
            join_policy=JoinPolicy.OPEN,
        )

        self.other_group = Group.objects.create(
            name='Group Two',
            description='Other group',
            owner=self.other_user,
            join_policy=JoinPolicy.OPEN,
        )

        GroupMember.objects.create(
            user=self.owner,
            group=self.group,
            role=RoleChoices.ADMIN,
        )

        self.folder = GroupFolder.objects.create(
            group=self.group,
            name='Folder One',
        )

        self.other_folder = GroupFolder.objects.create(
            group=self.other_group,
            name='Folder Two',
        )

        self.artwork = Artwork.objects.create(
            title='Artwork One',
            description='desc',
            image_url='https://example.com/art.jpg',
            type=ArtworkTypeChoices.PAINTING,
            user=self.owner,
        )

        self.folder.artworks.add(self.artwork)

    def test_get_queryset_does_not_allow_folder_from_another_group(self):
        self.client.login(username='owner', password='123pass123')

        response = self.client.get(
            reverse(
                'group-folder-edit',
                kwargs={'slug': self.group.slug, 'pk': self.other_folder.pk}
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_post_with_remove_artwork_from_folder_removes_artwork(self):
        self.client.login(username='owner', password='123pass123')

        response = self.client.post(
            reverse(
                'group-folder-edit',
                kwargs={'slug': self.group.slug, 'pk': self.folder.pk}
            ),
            data={'remove_artwork_from_folder': self.artwork.pk}
        )

        self.folder.refresh_from_db()
        self.assertNotIn(self.artwork, self.folder.artworks.all())

    def test_post_with_remove_artwork_from_folder_redirects_to_same_edit_page(self):
        self.client.login(username='owner', password='123pass123')

        response = self.client.post(
            reverse(
                'group-folder-edit',
                kwargs={'slug': self.group.slug, 'pk': self.folder.pk}
            ),
            data={'remove_artwork_from_folder': self.artwork.pk}
        )

        self.assertRedirects(
            response,
            reverse(
                'group-folder-edit',
                kwargs={'slug': self.group.slug, 'pk': self.folder.pk}
            )
        )

    def test_successful_edit_redirects_to_group_details(self):
        self.client.login(username='owner', password='123pass123')

        response = self.client.post(
            reverse(
                'group-folder-edit',
                kwargs={'slug': self.group.slug, 'pk': self.folder.pk}
            ),
            data={
                'name': 'Updated Folder',
                'description': 'Updated description',
            }
        )

        self.assertRedirects(
            response,
            reverse('group-details', kwargs={'slug': self.group.slug})
        )

        self.folder.refresh_from_db()
        self.assertEqual(self.folder.name, 'Updated Folder')