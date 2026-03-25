from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from artworks.models import Artwork
from groups.forms import GroupFolderForm
from groups.mixins import GroupAccessMixin
from groups.models import GroupFolder, Group

class GroupFolderCreateView(LoginRequiredMixin, GroupAccessMixin, UserPassesTestMixin, CreateView):
    model = GroupFolder
    form_class = GroupFolderForm
    template_name = 'groups/tabs/group-gallery.html'

    def get_group(self):
        return get_object_or_404(Group, slug=self.kwargs['slug'])

    def test_func(self):
        return self.user_is_group_staff(self.get_group(), self.request.user)

    def form_valid(self, form):
        form.instance.group = self.get_group()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('group-details', kwargs={'slug': self.kwargs['slug']})

class GroupFolderEditView(LoginRequiredMixin, GroupAccessMixin, UserPassesTestMixin, UpdateView):
    model = GroupFolder
    form_class = GroupFolderForm
    template_name = 'groups/group-folder-edit.html'
    context_object_name = 'folder'

    def get_group(self):
        return get_object_or_404(Group, slug=self.kwargs['slug'])

    def test_func(self):
        return self.user_is_group_staff(self.get_group(), self.request.user)

    def get_queryset(self):
        return GroupFolder.objects.filter(group=self.get_group())

    def get_success_url(self):
        return reverse_lazy('group-details', kwargs={'slug': self.kwargs['slug']})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        group = self.get_group()

        if 'remove_artwork_from_folder' in request.POST:
            artwork_pk = request.POST.get('remove_artwork_from_folder')
            artwork = get_object_or_404(self.object.artworks, pk=artwork_pk)
            self.object.artworks.remove(artwork)
            return redirect('group-folder-edit', slug=group.slug ,pk=self.object.pk)
        return super().post(request, *args, **kwargs)


class GroupFolderDetailView(DetailView):
    model = GroupFolder
    template_name = 'groups/group-folder-details.html'
    context_object_name = 'folder'

    def get_queryset(self):
        group = get_object_or_404(Group, slug=self.kwargs['slug'])
        return GroupFolder.objects.filter(group=group)


class GroupFolderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = GroupFolder

    def get_group(self):
        return get_object_or_404(Group, slug=self.kwargs['slug'])

    def test_func(self):
        return self.request.user == self.get_group().owner

    def get_queryset(self):
        return GroupFolder.objects.filter(group=self.get_group())

    def get_success_url(self):
        return reverse_lazy('group-details', kwargs={'slug': self.kwargs['slug']})

class MoveArtworkToFolderView(LoginRequiredMixin, GroupAccessMixin, UserPassesTestMixin, View):
    def test_func(self):
        group = get_object_or_404(Group, slug=self.kwargs['slug'])
        return self.user_is_group_staff(group, self.request.user)

    def post(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs['slug'])
        art_id = request.POST.get('art_id')
        folder_id = request.POST.get('folder_id')

        if not art_id or not folder_id:
            return redirect(request.META.get('HTTP_REFERER'))

        artwork = get_object_or_404(Artwork, pk=art_id)
        folder = get_object_or_404(GroupFolder, pk=folder_id, group=group)

        folder.artworks.add(artwork)

        return redirect(request.META.get('HTTP_REFERER'))