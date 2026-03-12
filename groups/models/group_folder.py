from django.db import models


class GroupFolder(models.Model):
    group = models.ForeignKey(
        'groups.Group',
        on_delete=models.CASCADE,
        related_name='folders'
    )

    name = models.CharField(
        max_length=100,
    )

    description = models.TextField(blank=True, null=True)

    artworks = models.ManyToManyField(
        'artworks.Artwork',
        related_name='group_folders',
        blank=True
    )

    class Meta:
        unique_together = ('group', 'name')

    def __str__(self):
        return self.name