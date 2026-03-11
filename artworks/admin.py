from django.contrib import admin
from artworks.models import Artwork, Tag


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    ...

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    ...
