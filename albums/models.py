from django.conf import settings
from django.db import models

class Album(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='albums',
    )
    artworks = models.ManyToManyField(
        'artworks.Artwork',
        related_name='albums',
        blank=True,
    )
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        unique_together = ('owner', 'name')
        ordering = ['-updated_at']

    def __str__(self):
        return self.name