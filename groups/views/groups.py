from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from artworks.models import Artwork
from common.mixins import OwnerOrPermissionsRequiredMixin
from groups.choices import RoleChoices, StatusChoices
from groups.forms import CreateGroupForm, EditGroupForm, GroupFolderForm
from groups.mixins import GroupAccessMixin
from groups.models import Group, GroupMember, GroupFolder, GroupJoinRequest, GroupSubmission, Post



class CreateGroupView(LoginRequiredMixin, CreateView):
    model = Group
    template_name = 'groups/group-form.html'
    form_class = CreateGroupForm

    def get_success_url(self):
        return reverse('group-details', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)

        GroupMember.objects.create(
            group=form.instance,
            role=RoleChoices.ADMIN,
            user=self.request.user
        )

        GroupFolder.objects.create(
            group=form.instance,
            name="Featured"
        )
        return response

class EditGroupView(LoginRequiredMixin, OwnerOrPermissionsRequiredMixin, UpdateView):
    model = Group
    template_name = 'groups/group-form.html'
    form_class = EditGroupForm
    permission_required = 'groups.change_group'
    owner_attr = 'owner'

    def get_success_url(self):
        return reverse('group-details', kwargs={'slug': self.object.slug})

class GroupDetailView(GroupAccessMixin, DetailView):
    model = Group
    template_name = 'groups/group-details.html'
    context_object_name = 'group'
    queryset = Group.objects.select_related('owner').prefetch_related(
        'artworks',
        'folders',
        'members__user',
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = self.object.members.exclude(user=self.object.owner).select_related('user')
        context['group_artworks'] = self.object.artworks.all()
        context['folders'] = self.object.folders.all()
        context['form'] = GroupFolderForm()
        context['group_members'] = GroupMember.objects.filter(group=self.object)
        context['join_requests'] = GroupJoinRequest.objects.filter(group=self.object, status=StatusChoices.PENDING)
        context['posts'] = Post.objects.filter(group=self.object)

        if self.request.user.is_authenticated:
            context['joined_to_group'] = self.object.members.filter(user=self.request.user.pk).exists()
            context['join_request_pending'] = GroupJoinRequest.objects.filter(
            group=self.object,
            user=self.request.user,
            status=StatusChoices.PENDING
            ).first()
            context['is_moderator_or_owner'] = self.user_is_group_staff(self.object, self.request.user)
        else:
            context['joined_to_group'] = False
            context['join_request_pending'] = None
            context['is_moderator_or_owner'] = False

        context['group_submissions'] = GroupSubmission.objects.filter(
            group=self.object,
            status=StatusChoices.PENDING
        )

        context['submissions_pending_count'] = context['group_submissions'].count()
        return context


class GroupListView(ListView):
    model = Group
    template_name = 'groups/groups-list.html'
    context_object_name = 'group_list'


class DeleteGroupView(LoginRequiredMixin, OwnerOrPermissionsRequiredMixin, DeleteView):
    model = Group
    permission_required = 'groups.delete_group'
    owner_attr = 'owner'

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.request.user.pk})

class RemoveArtworkFromGroupView(LoginRequiredMixin, GroupAccessMixin, UserPassesTestMixin, View):
    def get_group(self):
        return get_object_or_404(Group, slug=self.kwargs['slug'])

    def test_func(self):
        return self.user_is_group_staff(self.get_group(), self.request.user)

    def post(self, request, slug, artwork_pk):
        group = self.get_group()
        artwork = get_object_or_404(Artwork, pk=artwork_pk)

        if group.artworks.filter(pk=artwork.pk).exists():
            group.artworks.remove(artwork)

        folders = group.folders.filter(artworks=artwork)
        for folder in folders:
            folder.artworks.remove(artwork)

        return redirect('group-details', slug=group.slug)

