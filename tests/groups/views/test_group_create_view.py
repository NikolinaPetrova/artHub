from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from groups.choices import JoinPolicy, RoleChoices
from groups.models import Group, GroupMember, GroupFolder

UserModel = get_user_model()

class CreateGroupViewTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username="user1",
            email="user1@test.com",
            password="123pass123",
        )

    def test_create_group_sets_owner_and_redirects_to_details(self):
        self.client.login(username="user1", password="123pass123")
        response = self.client.post(
            reverse('create-group'),
            data={
                'name': 'digital',
                'description': 'test description',
                'join_policy': JoinPolicy.OPEN
            }
        )

        group = Group.objects.get(name='digital')
        self.assertEqual(group.owner, self.user)
        self.assertRedirects(
            response,
            reverse('group-details', kwargs={'slug': group.slug})
        )

    def test_create_group_creates_admin_membership_for_owner(self):
        self.client.login(username="user1", password="123pass123")
        self.client.post(
            reverse('create-group'),
            data={
                'name': 'digital',
                'description': 'test description',
                'join_policy': JoinPolicy.OPEN
            }
        )

        group = Group.objects.get(name='digital')
        self.assertTrue(
            GroupMember.objects.filter(
                group=group,
                user=self.user,
                role=RoleChoices.ADMIN
            ).exists()
        )

    def test_create_group_creates_featured_folder(self):
        self.client.login(username="user1", password="123pass123")
        self.client.post(
            reverse('create-group'),
            data={
                'name': 'digital',
                'description': 'test description',
                'join_policy': JoinPolicy.OPEN
            }
        )

        group = Group.objects.get(name='digital')
        self.assertTrue(
            GroupFolder.objects.filter(
                group=group,
                name='Featured'
            ).exists()
        )