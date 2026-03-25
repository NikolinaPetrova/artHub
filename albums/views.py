from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from albums.forms import AlbumCreateForm, AlbumEditForm
from albums.models import Album
from common.mixins import OwnerOrPermissionsRequiredMixin


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumCreateForm
    template_name = 'profile/profile-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['album_form'] = kwargs.get('album_form', self.get_form())
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile-details', kwargs={'pk': self.request.user.pk})

class AlbumDetailsView(DetailView):
    model = Album
    template_name = 'albums/album-details.html'
    context_object_name = 'album'

class AlbumEditView(LoginRequiredMixin, OwnerOrPermissionsRequiredMixin, UpdateView):
    model = Album
    form_class = AlbumEditForm
    template_name = 'albums/edit-album.html'
    permission_required = 'albums.change_album'
    owner_attr = 'owner'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if 'remove_artwork' in request.POST:
            artwork_pk = request.POST.get('remove_artwork')
            artwork = get_object_or_404(self.object.artworks, pk=artwork_pk)
            self.object.artworks.remove(artwork)
            return redirect('edit-album', pk=self.object.pk)

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('profile-details', kwargs={'pk': self.object.owner.pk})

class AlbumDeleteView(LoginRequiredMixin, OwnerOrPermissionsRequiredMixin, DeleteView):
    model = Album
    permission_required = 'albums.delete_album'
    owner_attr = 'owner'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.owner_pk = self.object.owner.pk
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('profile-details', kwargs={'pk': self.owner_pk})
