from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models


class Comment(models.Model):
    content = models.TextField(
        validators=[MinLengthValidator(2)]
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    artwork = models.ForeignKey(
        'artworks.Artwork',
        on_delete=models.CASCADE,
        related_name='comments',
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='child_replies',
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ('created_at',)

    @property
    def top_level(self):
        parent = self
        visited = set()
        while parent.parent:
            if parent.id in visited:
                break
            visited.add(parent.id)
            parent = parent.parent
        return parent

    def __str__(self):
        return f"Comment by {self.user.username}"