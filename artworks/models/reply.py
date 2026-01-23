from django.core.validators import MinLengthValidator
from django.db import models

from artworks.models import Comment


class Reply(models.Model):
    comment = models.ForeignKey(
        Comment,
        related_name='replies',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        'profiles.Profile',
        on_delete=models.CASCADE
    )
    content = models.TextField(
        validators=[MinLengthValidator(2)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.author}"