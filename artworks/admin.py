from django.contrib import admin
from artworks.models import Artwork, Tag, Comment, ArtworkLike


@admin.register(Artwork)
class ArtworkAdmin(admin.ModelAdmin):
    ...

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    ...

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    ...

@admin.register(ArtworkLike)
class LikeAdmin(admin.ModelAdmin):
    ...
