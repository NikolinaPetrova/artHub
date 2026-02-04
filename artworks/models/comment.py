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

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    @property
    def top_level_replies(self):
        return self.replies.filter(parent__isnull=True)

    def __str__(self):
        return f"Comment by {self.user.username}"