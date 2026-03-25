from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from artworks.forms import CreateArtworkForm, EditArtworkForm, DeleteArtworkForm
from artworks.models import Artwork
from common.mixins import OwnerOrPermissionsRequiredMixin, UserInFormKwargsMixin
from interactions.forms.comment_form import CreateCommentForm, ReplyForm, CommentEditForm


class CreateArtworkView(LoginRequiredMixin, UserInFormKwargsMixin, CreateView):
    model = Artwork
    form_class = CreateArtworkForm
    template_name = 'artwork/create-artwork.html'
    success_url = reverse_lazy('gallery')


class ArtworkDetailsView(DetailView):
    model = Artwork
    template_name = 'artwork/artwork-details.html'
    context_object_name = 'artwork'

    def get_queryset(self):
        return (
            Artwork.objects
            .select_related('user')
            .prefetch_related(
                'tags',
                'albums',
                'likes',
                'comments__user',
                'comments__child_replies__user',
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artwork = self.object
        user = self.request.user

        context['comment_form'] = CreateCommentForm()
        context['reply_form'] = ReplyForm(initial={'artwork': artwork.pk})
        context['edit_form'] = CommentEditForm()
        context['user_like'] = artwork.likes.filter(user=user).exists() if user.is_authenticated else False
        context['comments'] = artwork.comments.filter(parent__isnull=True)
        return context

class EditArtworkView(LoginRequiredMixin, OwnerOrPermissionsRequiredMixin, UserInFormKwargsMixin, UpdateView):
    model = Artwork
    template_name = 'artwork/edit-artwork.html'
    form_class = EditArtworkForm
    permission_required = 'artworks.change_artwork'
    owner_attr = 'user'

    def get_success_url(self):
        return reverse('artwork-details', kwargs={'pk': self.object.pk})

class DeleteArtworkView(LoginRequiredMixin, OwnerOrPermissionsRequiredMixin, UserInFormKwargsMixin, DeleteView):
    model = Artwork
    form_class = DeleteArtworkForm
    template_name = 'artwork/delete-artwork.html'
    permission_required = 'artworks.delete_artwork'
    owner_attr = 'user'

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(instance=self.get_object(), **self.get_form_kwargs())

    def post(self, request, *args, **kwargs):
        choice = request.POST.get('confirm')
        artwork = self.get_object()
        if choice == 'yes':
            artwork.delete()
            return HttpResponseRedirect(reverse_lazy('gallery'))

        return HttpResponseRedirect(reverse_lazy('artwork-details', kwargs={'pk': artwork.pk}))