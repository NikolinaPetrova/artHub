from django.db.models import Q
from django.views.generic import TemplateView, ListView

from artworks.models import Artwork
from common.utils import get_profile


class HomePageView(TemplateView):
    template_name = 'common/home-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_profile'] = get_profile()
        return context

class Custom404View(TemplateView):
    template_name = 'common/404.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['status'] = 404
        return super().render_to_response(context, **response_kwargs)

class SearchArtworksView(ListView):
    model = Artwork
    template_name = 'artwork/gallery.html'
    context_object_name = 'artwork_list'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Artwork.objects.filter(Q(title__icontains=query) | Q(tags__name__icontains=query)).distinct()
        return Artwork.objects.all()