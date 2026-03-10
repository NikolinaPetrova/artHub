from django.db import models
from groups.choices import StatusChoices


class GroupSubmission(models.Model):
    group = models.ForeignKey(
        'groups.Group',
        on_delete=models.CASCADE,
        related_name='submissions'
    )

    artwork = models.ForeignKey(
        'artworks.Artwork',
        on_delete=models.CASCADE,
        related_name='group_submissions'
    )

    folder = models.ForeignKey(
        'groups.GroupFolder',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    submitted_by = models.ForeignKey(
        'accounts.ArtHubUser',
        on_delete=models.CASCADE,
        related_name='group_submissions'
    )

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default='pending'
    )

    submitted_at = models.DateTimeField(auto_now_add=True)

    reviewed_by = models.ForeignKey(
        'accounts.ArtHubUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_group_submissions'
    )

    class Meta:
        unique_together = ('group', 'artwork')

    def __str__(self):
        return f"{self.artwork} submission to {self.group} ({self.status})"