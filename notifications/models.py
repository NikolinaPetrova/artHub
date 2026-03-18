from django.db import models
from notifications.choices import NotificationsChoices


class Notification(models.Model):
    recipient = models.ForeignKey(
        'accounts.ArtHubUser',
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    sender = models.ForeignKey(
        'accounts.ArtHubUser',
        on_delete=models.CASCADE,
        related_name="sent_notifications"
    )

    notification_type = models.CharField(max_length=50, choices=NotificationsChoices.choices)

    artwork = models.ForeignKey(
        'artworks.Artwork',
        null=True, blank=True,
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        'groups.Post',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    comment = models.ForeignKey(
        'interactions.Comment',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    message = models.CharField(max_length=255)
    target_url = models.CharField(max_length=255, blank=True)

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)