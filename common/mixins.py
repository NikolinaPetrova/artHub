from django.contrib.auth.mixins import UserPassesTestMixin
from django.db import models
from django.shortcuts import redirect
from django.utils.text import slugify


class DisabledFormFieldsMixin:
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].disabled = True


class SlugMixin(models.Model):
    slug = models.SlugField(
        max_length=250,
        unique=True,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug and hasattr(self, 'name'):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

from django.db import models

class CreatedAtMixin(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        abstract = True


class OwnerOrPermissionsRequiredMixin(UserPassesTestMixin):
    permission_required = None
    owner_attr = 'owner'

    def handle_no_permission(self):
        return redirect('home')

    def has_elevated_permission(self, user):
        return (
            user.is_authenticated and
            self.permission_required and
            user.has_perm(self.permission_required)
        )

    def is_owner(self, user, obj):
        return user.is_authenticated and user == getattr(obj, self.owner_attr, None)

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        return self.is_owner(user, obj) or self.has_elevated_permission(user)

    def get_queryset(self):
        user = self.request.user

        if self.has_elevated_permission(user):
            return self.model.objects.all()

        lookup = {self.owner_attr: user}
        return self.model.objects.filter(**lookup)

class UserInFormKwargsMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

