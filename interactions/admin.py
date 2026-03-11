from django.contrib import admin
from interactions.models import Comment, Like


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    ...

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    ...