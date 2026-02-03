from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        blank=True,
    )

    def __str__(self):
        return self.name