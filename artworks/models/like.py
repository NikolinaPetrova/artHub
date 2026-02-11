from django.conf import settings
from django.db import models
from artworks.mixins import CreatedAtMixin


class ArtworkLike(CreatedAtMixin):
    artwork = models.ForeignKey(
        'artworks.Artwork',
        on_delete=models.CASCADE,
        related_name='likes',
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes',
    )

    class Meta:
        unique_together = ('artwork', 'user')

    def __str__(self):
        return f"{self.artwork} liked by {self.user}"