import re
from django.db.models import Q
from django.views.generic import ListView
from artworks.models import Artwork, Tag


class GalleryPageView(ListView):
    model = Artwork
    template_name = 'artwork/gallery.html'

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        queryset = Artwork.objects.select_related('user').prefetch_related('tags')

        if not query:
            return queryset

        search_words = re.findall(r'\w+', query)

        q_object = Q()

        for word in search_words:
            q_object |= Q(title__icontains=word)
            q_object |= Q(tags__name__icontains=word)

        return queryset.filter(q_object).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context