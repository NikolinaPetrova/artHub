from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models


class Reply(models.Model):
    comment = models.ForeignKey(
        'artworks.Comment',
        related_name='replies',
        on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='child_replies'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='replies',
    )
    content = models.TextField(
        validators=[MinLengthValidator(2)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user.username}"