from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from artworks.models import Artwork
from interactions.models import Like


class ArtworkLikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        artwork = get_object_or_404(Artwork, pk=pk)
        user = self.request.user

        like, created = Like.objects.get_or_create(artwork=artwork, user=user)

        if not created:
            like.delete()

        return redirect('artwork-details', pk=artwork.pk)