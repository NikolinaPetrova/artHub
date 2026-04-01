from cloudinary.models import CloudinaryField
from django.db import models
from common.mixins import SlugMixin
from groups.choices import JoinPolicy


class Group(SlugMixin):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(
        'accounts.ArtHubUser',
        on_delete=models.CASCADE,
        related_name='owned_groups',
    )

    avatar = CloudinaryField('image', blank=True, null=True)
    banner = CloudinaryField('image', blank=True, null=True)
    join_policy = models.CharField(
        max_length=20,
        choices=JoinPolicy.choices,
        default=JoinPolicy.OPEN
    )
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name