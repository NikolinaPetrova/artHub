import re
from django.db.models import Q
from django.views.generic import TemplateView, ListView
from artworks.models import Artwork


class HomePageView(ListView):
    model = Artwork
    template_name = 'common/home-page.html'

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

class Custom404View(TemplateView):
    template_name = '404.html'

    def render_to_response(self, context, **response_kwargs):
        response_kwargs['status'] = 404
        return super().render_to_response(context, **response_kwargs)
