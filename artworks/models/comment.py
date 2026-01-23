from django.core.validators import MinLengthValidator
from django.db import models


class Comment(models.Model):
    content = models.TextField(
        validators=[MinLengthValidator(2)]
    )

    author = models.ForeignKey(
        'profiles.Profile',
        on_delete=models.CASCADE,
        related_name='comments',
    )

    artwork = models.ForeignKey(
        'artworks.Artwork',
        on_delete=models.CASCADE,
        related_name='comments',
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"Comment by {self.author}"