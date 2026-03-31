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
        constraints = [

            models.UniqueConstraint(
                fields=['user', 'artwork'],
                name='unique_user_artwork_like'
            ),

            models.UniqueConstraint(
                fields=['user', 'post'],
                name='unique_user_post_like'
            ),

            models.UniqueConstraint(
                fields=['user', 'comment'],
                name='unique_user_comment_like'
            ),

            models.CheckConstraint(
                condition=(
                        models.Q(artwork__isnull=False, post__isnull=True, comment__isnull=True) |
                        models.Q(artwork__isnull=True, post__isnull=False, comment__isnull=True) |
                        models.Q(artwork__isnull=True, post__isnull=True, comment__isnull=False)
                ),
                name='like_target_constraint'
            ),
        ]

    def __str__(self):
        return f"{self.artwork} liked by {self.user}"