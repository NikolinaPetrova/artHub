from django.conf import settings
from django.db import models
from common.mixins import CreatedAtMixin


class Like(CreatedAtMixin):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes',
    )

    artwork = models.ForeignKey(
        'artworks.Artwork',
        on_delete=models.CASCADE,
        related_name='likes',
        null=True,
        blank=True,
    )

    post = models.ForeignKey(
        'groups.Post',
        on_delete=models.CASCADE,
        related_name='likes',
        null=True,
        blank=True,
    )

    comment = models.ForeignKey(
        'interactions.Comment',
        on_delete=models.CASCADE,
        related_name='likes',
        null=True,
        blank=True,
    )

    class Meta:
        unique_together = ('artwork', 'user')

    def __str__(self):
        return f"{self.artwork} liked by {self.user}"