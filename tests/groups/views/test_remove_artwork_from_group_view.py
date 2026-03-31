from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from artworks.choices import ArtworkTypeChoices
from artworks.models import Artwork
from groups.choices import JoinPolicy, RoleChoices
from groups.models import Group, GroupMember, GroupFolder

UserModel = get_user_model()


class RemoveArtworkFromGroupViewTests(TestCase):
    def setUp(self):
        self.owner = UserModel.objects.create_user(
            username="owner",
            email="owner@test.com",
            password="123pass123"
        )

        self.member = UserModel.objects.create_user(
            username="member",
            email="member@test.com",
            password="123pass123"
        )

        self.other_user = UserModel.objects.create_user(
            username="other",
            email="other@test.com",
            password="123pass123"
        )

        self.group = Group.objects.create(
            name="group1",
            description="test group",
            owner=self.owner,
            join_policy=JoinPolicy.OPEN,
        )

        GroupMember.objects.create(
            user=self.owner,
            group=self.group,
            role=RoleChoices.ADMIN,
        )

        GroupMember.objects.create(
            user=self.member,
            group=self.group,
            role=RoleChoices.MEMBER,
        )

        self.artwork = Artwork.objects.create(
            title="test artwork",
            description="test artwork",
            image_url='https://example.com/artwork.jpg',
            type=ArtworkTypeChoices.PAINTING,
            user=self.owner,
        )

        self.group.artworks.add(self.artwork)

        self.folder1 = GroupFolder.objects.create(
            group=self.group,
            name='folder1'
        )

        self.folder2 = GroupFolder.objects.create(
            group=self.group,
            name='folder2'
        )

        self.folder1.artworks.add(self.artwork)
        self.folder2.artworks.add(self.artwork)

        self.url = reverse(
            'group-remove-artwork',
            kwargs={'slug': self.group.slug, 'artwork_pk': self.artwork.pk}
        )

    def test_staff_can_remove_artwork_from_group_and_group_folders(self):
        self.client.login(username="owner", password="123pass123")
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            reverse('group-details', kwargs={'slug': self.group.slug})
        )

        self.assertFalse(self.group.artworks.filter(pk=self.artwork.pk).exists())
        self.assertFalse(self.folder1.artworks.filter(pk=self.artwork.pk).exists())
        self.assertFalse(self.folder2.artworks.filter(pk=self.artwork.pk).exists())

    def test_post_removes_artwork_from_folders_when_artwork_is_in_group(self):
        self.client.login(username='owner', password='123pass123')
        self.client.post(self.url)
        self.assertEqual(self.folder1.artworks.count(), 0)
        self.assertEqual(self.folder2.artworks.count(), 0)

    def test_post_redirects_when_artwork_is_not_in_group(self):
        self.client.login(username='owner', password='123pass123')
        self.group.artworks.remove(self.artwork)
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            reverse('group-details', kwargs={'slug': self.group.slug})
        )

    def test_non_staff_cannot_remove_artwork_from_group(self):
        self.client.login(username='member', password='123pass123')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)