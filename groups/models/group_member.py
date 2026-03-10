from django.db import models
from groups.choices import RoleChoices


class GroupMember(models.Model):
    user = models.ForeignKey(
        'accounts.ArtHubUser',
        on_delete=models.CASCADE,
        related_name='group_memberships'
    )

    group = models.ForeignKey(
        'groups.Group',
        on_delete=models.CASCADE,
        related_name='members',
        null=True,
        blank=True
    )

    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.MEMBER
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'group')

    def __str__(self):
        return f"{self.user} in {self.group}"