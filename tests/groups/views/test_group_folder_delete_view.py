from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from groups.models import Group, GroupFolder
from groups.choices import JoinPolicy

UserModel = get_user_model()


class GroupFolderDeleteViewTests(TestCase):
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

        self.folder = GroupFolder.objects.create(
            group=self.group,
            name='Folder One',
        )

        self.other_folder = GroupFolder.objects.create(
            group=self.other_group,
            name='Folder Two',
        )

    def test_owner_can_delete_folder(self):
        self.client.login(username='owner', password='123pass123')

        response = self.client.post(
            reverse(
                'group-folder-delete',
                kwargs={'slug': self.group.slug, 'pk': self.folder.pk}
            )
        )

        self.assertRedirects(
            response,
            reverse('group-details', kwargs={'slug': self.group.slug})
        )

        self.assertFalse(GroupFolder.objects.filter(pk=self.folder.pk).exists())

    def test_non_owner_cannot_delete_folder(self):
        self.client.login(username='other', password='123pass123')

        response = self.client.post(
            reverse(
                'group-folder-delete',
                kwargs={'slug': self.group.slug, 'pk': self.folder.pk}
            )
        )

        self.assertEqual(response.status_code, 403)

    def test_cannot_delete_folder_from_another_group(self):
        self.client.login(username='owner', password='123pass123')

        response = self.client.post(
            reverse(
                'group-folder-delete',
                kwargs={'slug': self.group.slug, 'pk': self.other_folder.pk}
            )
        )

        self.assertEqual(response.status_code, 404)