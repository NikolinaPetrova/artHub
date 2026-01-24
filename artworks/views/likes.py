from django.shortcuts import get_object_or_404, redirect
from django.views import View
from artworks.models import Artwork, ArtworkLike
from common.utils import get_profile


class ArtworkLikeView(View):
    def post(self, request, pk):
        artwork = get_object_or_404(Artwork, pk=pk)
        profile = get_profile()

        like, created = ArtworkLike.objects.get_or_create(artwork=artwork, profile=profile)

        if not created:
            like.delete()

        return redirect('artwork-details', pk=artwork.pk)