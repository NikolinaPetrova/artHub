from django.db import models
from artHub import settings
from common.mixins import CreatedAtMixin


class Post(CreatedAtMixin):
    group = models.ForeignKey(
        'groups.Group',
        on_delete=models.CASCADE,
        related_name='posts'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(
        upload_to='post_images',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['-created_at']