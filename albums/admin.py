from django.contrib import admin
from albums.models import Album


@admin.register(Album)
class ArtHubAdmin(admin.ModelAdmin):
    ...
