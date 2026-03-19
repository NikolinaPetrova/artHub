from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView

from artworks.models import Artwork
from groups.choices import RoleChoices, StatusChoices
from groups.forms import CreateGroupForm, EditGroupForm, GroupFolderForm
from groups.models import Group, GroupMember, GroupFolder, GroupJoinRequest, GroupSubmission, Post
from interactions.forms import CreateCommentForm, ReplyForm, CommentEditForm


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

class EditGroupView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Group
    template_name = 'groups/group-form.html'
    form_class = EditGroupForm

    def test_func(self):
        return self.request.user == self.get_object().owner

    def get_success_url(self):
        return reverse('group-details', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class GroupDetailView(DetailView):
    model = Group
    template_name = 'groups/group-details.html'
    context_object_name = 'group'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = self.object.members.exclude(user=self.object.owner).select_related('user')
        context['group_artworks'] = self.object.artworks.all()
        context['folders'] = self.object.folders.all()
        context['form'] = GroupFolderForm()
        context['group_members'] = GroupMember.objects.filter(group=self.object)
        context['join_requests'] = GroupJoinRequest.objects.filter(group=self.object, status=StatusChoices.PENDING)
        context['posts'] = Post.objects.filter(group=self.object)
        membership = self.object.members.filter(user=self.request.user).first()
        context['is_moderator_or_owner'] = (
                self.request.user == self.object.owner or
                (membership and membership.role in [RoleChoices.ADMIN, RoleChoices.MODERATOR])
        )

        if self.request.user.is_authenticated:
            context['joined_to_group'] = self.object.members.filter(user=self.request.user.pk).exists()
            context['join_request_pending'] = GroupJoinRequest.objects.filter(
            group=self.object,
            user=self.request.user,
            status='pending'
            ).first()
        else:
            context['joined_to_group'] = None
            context['join_request_pending'] = None

        context['group_submissions'] = GroupSubmission.objects.filter(
            group=self.object,
            status=StatusChoices.PENDING
        )

        context['submissions_pending_count'] = GroupSubmission.objects.filter(
            group=self.object,
            status=StatusChoices.PENDING
        ).count()
        return context


class GroupListView(ListView):
    model = Group
    template_name = 'profile/tabs/profile-groups.html'
    context_object_name = 'group_list'

    def get_queryset(self):
        return self.request.user.groups.all()

class DeleteGroupView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Group

    def test_func(self):
        group = self.get_object()
        return self.request.user == group.owner or self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.request.user.pk})


class RemoveArtworkFromGroupView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        group = get_object_or_404(Group, slug=self.kwargs['slug'])
        membership = group.members.filter(user=self.request.user).first()
        is_admin_or_moderator = (
            self.request.user == group.owner or
            (membership and membership.role in [RoleChoices.ADMIN, RoleChoices.MODERATOR])
        )
        return is_admin_or_moderator

    def post(self, request, slug, artwork_pk):
        group = get_object_or_404(Group, slug=slug)
        artwork = get_object_or_404(Artwork, pk=artwork_pk)

        if artwork in group.artworks.all():
            group.artworks.remove(artwork)

        folders = group.folders.filter(artworks=artwork)
        for folder in folders:
            folder.artworks.remove(artwork)

        return redirect('group-details', slug=group.slug)

