from django.contrib.auth import get_user_model
from django.test import TestCase
from groups.choices import JoinPolicy
from groups.forms import CreateGroupForm
from groups.models import Group

UserModel = get_user_model()

class CreateGroupFormTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='owner',
            email='owner@test.com',
            password='123pass123'
        )

    def test_form_is_valid_when_name_is_unique(self):
        form = CreateGroupForm(
            data={
                'name': 'digital',
                'description': 'test description',

                'join_policy': JoinPolicy.OPEN
            }
        )

        self.assertTrue(form.is_valid())

    def test_form_is_invalid_when_group_with_same_name_already_exists(self):
        Group.objects.create(
            name='digital',
            description='test description',
            join_policy=JoinPolicy.OPEN,
            owner=self.user,
        )

        form = CreateGroupForm(
            data={
                'name': 'digital',
                'description': 'test description 2',
                'join_policy': JoinPolicy.OPEN,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('A group with this name already exists', form.errors['name'])

    def test_clean_name_returns_name_when_it_is_unique(self):
        form = CreateGroupForm(
            data={
                'name': 'unique',
                'description': 'test description',
                'join_policy': JoinPolicy.OPEN,
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['name'], 'unique')