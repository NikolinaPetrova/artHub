from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.http import Http404
from django.test import TestCase, RequestFactory
from django.views.generic import DetailView
from artworks.choices import ArtworkTypeChoices
from artworks.models import Artwork
from common.mixins import OwnerOrPermissionsRequiredMixin

UserModel = get_user_model()

class TestView(OwnerOrPermissionsRequiredMixin, DetailView):
    model = Artwork
    permission_required = 'artworks.change_artwork'
    owner_attr = 'user'

class OwnerOrPermissionsMixinTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.owner = UserModel.objects.create_user(
            username='owner',
            email='owner@test.com',
            password='123pass123'
        )
        self.other_user = UserModel.objects.create_user(
            username='other',
            email='other@test.com',
            password='123pass123'
        )

        self.artwork = Artwork.objects.create(
            title='Test',
            description='test',
            image_url='https://example.com/img.jpg',
            type=ArtworkTypeChoices.PHOTOGRAPHY,
            user=self.owner,
        )

    def test_is_owner_returns_true_for_owner(self):
        view = TestView()
        self.assertTrue(view.is_owner(self.owner, self.artwork))

    def test_is_owner_returns_false_for_non_owner(self):
        view = TestView()
        self.assertFalse(view.is_owner(self.other_user, self.artwork))

    def test_has_elevated_permission_returns_true(self):
        permission = Permission.objects.get(codename='change_artwork')
        self.other_user.user_permissions.add(permission)

        view = TestView()
        self.assertTrue(view.has_elevated_permission(self.other_user))

    def test_test_func_allows_owner(self):
        request = self.factory.get('/')
        request.user = self.owner

        view = TestView()
        view.request = request
        view.kwargs = {'pk': self.artwork.pk}

        self.assertTrue(view.test_func())

    def test_test_func_raises_404_for_non_owner_without_permission(self):
        request = self.factory.get('/')
        request.user = self.other_user

        view = TestView()
        view.request = request
        view.kwargs = {'pk': self.artwork.pk}

        with self.assertRaises(Http404):
            view.test_func()

    def test_get_queryset_returns_only_user_objects(self):
        other_artwork = Artwork.objects.create(
            title='Other',
            description='test',
            image_url='https://example.com/other.jpg',
            type=ArtworkTypeChoices.PHOTOGRAPHY,
            user=self.other_user,
        )

        request = self.factory.get('/')
        request.user = self.owner

        view = TestView()
        view.request = request
        view.model = Artwork

        queryset = view.get_queryset()

        self.assertIn(self.artwork, queryset)
        self.assertNotIn(other_artwork, queryset)