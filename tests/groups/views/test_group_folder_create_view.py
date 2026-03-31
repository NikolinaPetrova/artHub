from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from groups.choices import JoinPolicy, RoleChoices
from groups.models import Group, GroupMember, GroupFolder

UserModel = get_user_model()

class GroupFolderCreateViewTest(TestCase):
    def setUp(self):
        self.owner = UserModel.objects.create_user(
            username='owner',
            email='owner@test.com',
            password='123pass123',
        )

        self.member = UserModel.objects.create_user(
            username='member',
            email='member@test.com',
            password='123pass123',
        )

        self.group = Group.objects.create(
            name='digital',
            description='test description',
            owner=self.owner,
            join_policy=JoinPolicy.OPEN,
        )

        GroupMember.objects.create(
            user=self.owner,
            group=self.group,
            role=RoleChoices.ADMIN
        )

        GroupMember.objects.create(
            user=self.member,
            group=self.group,
            role=RoleChoices.MEMBER
        )

    def test_group_staff_can_create_folder(self):
        self.client.login(username='owner', password='123pass123')
        response = self.client.post(
            reverse('group-folder-create', kwargs={'slug': self.group.slug}),
            data={
                'name': 'test folder',
                'description': 'test description',
            }
        )

        self.assertEqual(response.status_code, 302)

    def test_form_valid_sets_group_to_created_folder(self):
        self.client.login(username='owner', password='123pass123')
        response = self.client.post(
            reverse('group-folder-create', kwargs={'slug': self.group.slug}),
            data={
                'name': 'test folder',
                'description': 'test description',
            }
        )

        self.assertRedirects(
            response,
            reverse('group-details', kwargs={'slug': self.group.slug})
        )
        folder = GroupFolder.objects.get(name='test folder')
        self.assertEqual(folder.group, self.group)

    def test_get_success_url_redirects_to_group_details(self):
        self.client.login(username='owner', password='123pass123')
        response = self.client.post(
            reverse('group-folder-create', kwargs={'slug': self.group.slug}),
            data={
                'name': 'test folder',
                'description': 'test description',
            }
        )

        self.assertRedirects(
            response,
            reverse('group-details', kwargs={'slug': self.group.slug})
        )