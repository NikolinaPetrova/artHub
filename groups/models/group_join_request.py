from django.db import models
from groups.choices import StatusChoices


class GroupJoinRequest(models.Model):
    user = models.ForeignKey(
        'accounts.ArtHubUser',
        on_delete=models.CASCADE,
    )

    group = models.ForeignKey(
        'groups.Group',
        on_delete=models.CASCADE,
        related_name='join_requests'
    )

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'group')

    def __str__(self):
        return f"{self.user} -> {self.group} ({self.status})"