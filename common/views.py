import re
from django.db.models import Q, Count
from django.views.generic import TemplateView, ListView
from artworks.models import Artwork


class HomePageView(ListView):
    model = Artwork
    template_name = 'common/home-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_artworks'] = Artwork.objects.annotate(
            likes_count=Count('likes', distinct=True)
        ).order_by('-likes_count')[:5]
        return context

class Custom404View(TemplateView):
    template_name = '404.html'

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['status'] = 404
        return super().render_to_response(context, **response_kwargs)
