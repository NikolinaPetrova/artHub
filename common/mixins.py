from django.db import models
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
