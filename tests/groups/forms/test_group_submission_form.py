from django.contrib.auth import get_user_model
from django.test import TestCase
from artworks.choices import ArtworkTypeChoices
from artworks.models import Artwork
from groups.choices import JoinPolicy
from groups.forms import GroupSubmissionForm
from groups.models import Group, GroupFolder

UserModel = get_user_model()

class GroupSubmissionFormTests(TestCase):
    def setUp(self):
        self.user1 = UserModel.objects.create_user(
            username="user1",
            email="user1@test.com",
            password="123pass123"
        )

        self.user2 = UserModel.objects.create_user(
            username="user2",
            email='user2@test.com',
            password="123pass123"
        )

        self.group1 = Group.objects.create(
            name='group1',
            description='test description',
            owner=self.user1,
            join_policy=JoinPolicy.OPEN,
        )

        self.group2 = Group.objects.create(
            name='group2',
            description='test description',
            owner=self.user2,
            join_policy=JoinPolicy.OPEN,
        )

        self.artwork1 = Artwork.objects.create(
            title='artwork1',
            description='test artwork1',
            image_url = 'https://example.com/artwork1.jpg',
            type=ArtworkTypeChoices.PAINTING,
            user=self.user1,
        )

        self.artwork2 = Artwork.objects.create(
            title='artwork2',
            description='test artwork2',
            image_url = 'https://example.com/artwork2.jpg',
            type=ArtworkTypeChoices.PAINTING,
            user=self.user2,
        )

        self.folder1 = GroupFolder.objects.create(
            group=self.group1,
            name='folder1',
        )

        self.folder2 = GroupFolder.objects.create(
            group=self.group2,
            name='folder2',
        )

    def test_artwork_field_queryset_contains_only_user_artworks(self):
        form = GroupSubmissionForm(
            user=self.user1,
            group=self.group1,
        )

        self.assertIn(self.artwork1, form.fields['artwork'].queryset)
        self.assertNotIn(self.artwork2, form.fields['artwork'].queryset)

    def test_folder_field_queryset_contains_only_group_folders(self):
        form = GroupSubmissionForm(
            user=self.user1,
            group=self.group1,
        )

        self.assertIn(self.folder1, form.fields['folder'].queryset)
        self.assertNotIn(self.folder2, form.fields['folder'].queryset)