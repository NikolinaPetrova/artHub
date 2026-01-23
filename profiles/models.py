from django.db import models
from profiles.validators import UsernameValidator


class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[UsernameValidator()]
    )
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    professional_artist = models.BooleanField(
        default=False,
        help_text="Check if you create art professionally."
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'