from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models
from artworks.choices import ArtworkTypeChoices
from artworks.mixins import CreatedAtMixin


class Artwork(CreatedAtMixin):
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(3)],
        help_text="Give your artwork a descriptive title."
    )
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField()
    type = models.CharField(
        max_length=20,
        choices=ArtworkTypeChoices.choices,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='artworks',
    )

    tags = models.ManyToManyField(
        'artworks.Tag',
        related_name='artworks',
        blank=True,
    )

    def __str__(self):
        return self.title