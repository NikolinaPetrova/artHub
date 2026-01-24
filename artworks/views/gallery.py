from django.views.generic import ListView
from artworks.models import Artwork

class GalleryPageView(ListView):
    model = Artwork
    template_name = 'artwork/gallery.html'