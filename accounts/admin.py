from django.contrib import admin
from accounts.models import ArtHubUser

@admin.register(ArtHubUser)
class ArtHubAdmin(admin.ModelAdmin):
    ...
