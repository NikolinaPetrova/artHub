from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from albums.forms import AlbumCreateForm, AlbumEditForm
from albums.models import Album
from artworks.models import Artwork


class AlbumCreateView(CreateView):
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

class AlbumEditView(UpdateView):
    model = Album
    form_class = AlbumEditForm
    template_name = 'albums/edit-album.html'

    def get_queryset(self):
        return Album.objects.filter(owner=self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if 'remove_artwork' in request.POST:
            artwork_pk = request.POST.get('remove_artwork')
            artwork = get_object_or_404(self.object.artworks, pk=artwork_pk)
            self.object.artworks.remove(artwork)
            return redirect('edit-album', pk=self.object.pk)

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('profile-details', kwargs={'pk': self.request.user.pk})

class AlbumDeleteView(DeleteView):
    model = Album

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_queryset(self):
        return Album.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse('profile-details', kwargs={'pk': self.request.user.pk})
