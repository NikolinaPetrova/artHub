from django.db import models


class ArtworkTypeChoices(models.TextChoices):
    DIGITAL = 'Digital', 'Digital'
    PAINTING = 'Painting', 'Painting'
    DRAWING = 'Drawing', 'Drawing'
    PHOTOGRAPHY = 'Photography', 'Photography'
