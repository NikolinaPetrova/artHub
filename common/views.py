from django.db.models import Q
from django.views.generic import TemplateView, ListView
from artworks.models import Artwork


class HomePageView(TemplateView):
    template_name = 'common/home-page.html'

class Custom404View(TemplateView):
    template_name = 'common/404.html'

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['status'] = 404
        return super().render_to_response(context, **response_kwargs)

class SearchArtworksView(ListView):
    model = Artwork
    template_name = 'artwork/gallery.html'
    context_object_name = 'artwork_list'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        queryset = Artwork.objects.prefetch_related('tags')
        if query:
            return queryset.filter(Q(title__icontains=query) | Q(tags__name__icontains=query)).distinct()
        return queryset