import re
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView
from artworks.models import Artwork, Tag


class GalleryPageView(ListView):
    model = Artwork
    template_name = 'artwork/gallery.html'
    paginate_by = 8

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

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string(
                'artwork/artwork_items.html',
                {'artwork_list': context['artwork_list']},
                request=self.request,
            )

            return JsonResponse({
                'html': html,
                'has_next': context['page_obj'].has_next(),
                'next_page_number': context['page_obj'].next_page_number() if context['page_obj'].has_next() else None,
            })

        return super().render_to_response(context, **response_kwargs)