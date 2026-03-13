from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from artworks.forms import CreateArtworkForm, EditArtworkForm, DeleteArtworkForm
from artworks.models import Artwork
from interactions.forms.comment_form import CreateCommentForm, ReplyForm, CommentEditForm
from interactions.models import Comment


class CreateArtworkView(LoginRequiredMixin, CreateView):
    model = Artwork
    form_class = CreateArtworkForm
    template_name = 'artwork/create-artwork.html'
    success_url = reverse_lazy('gallery')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


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

class EditArtworkView(LoginRequiredMixin, UpdateView):
    model = Artwork
    template_name = 'artwork/edit-artwork.html'
    form_class = EditArtworkForm

    def get_form_kwargs(self, form_class=None):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('artwork-details', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        return Artwork.objects.filter(user=self.request.user)

class DeleteArtworkView(LoginRequiredMixin, DeleteView):
    model = Artwork
    form_class = DeleteArtworkForm
    template_name = 'artwork/delete-artwork.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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
        else:
            return HttpResponseRedirect(reverse_lazy('artwork-details', kwargs={'pk': artwork.pk}))

    def get_queryset(self):
        return Artwork.objects.filter(user=self.request.user)