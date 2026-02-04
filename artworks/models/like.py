from django.conf import settings
from django.db import models

class ArtworkLike(models.Model):
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

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        unique_together = ('artwork', 'user')

    def __str__(self):
        return f"{self.artwork} liked by {self.user}"