from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, DeleteView
from groups.choices import RoleChoices, JoinPolicy, StatusChoices
from groups.forms import GroupMemberForm
from groups.mixins import GroupAccessMixin
from groups.models import Group, GroupMember, GroupJoinRequest
from notifications.services import NotificationService


class ToggleGroupMembershipView(LoginRequiredMixin, View):
    def post(self, request, slug, *args, **kwargs):
        group = get_object_or_404(Group, slug=slug)
        membership = GroupMember.objects.filter(group=group, user=request.user).first()

        if membership:
            if request.user == group.owner:
                return redirect('group-details', slug=slug)

            membership.delete()
            messages.success(request, "You have left the group.")
        else:
            if group.join_policy == JoinPolicy.APPROVAL:
                if GroupJoinRequest.objects.filter(group=group, user=request.user, status=StatusChoices.PENDING).exists():
                    messages.info(request, "Your join request is already pending.")
                if GroupJoinRequest.objects.filter(group=group, user=request.user, status=StatusChoices.REJECTED).exists():
                    messages.error(request, 'You have been rejected from joining the group.')
                else:
                    GroupJoinRequest.objects.create(group=group, user=request.user)
                    NotificationService.notify_join_request(request.user, group)
            else:
                GroupMember.objects.create(group=group, user=request.user)
                NotificationService.notify_join_to_public_group(request.user, group)

        return redirect('group-details', slug=slug)

class ChangeMemberRoleView(LoginRequiredMixin, GroupAccessMixin, UserPassesTestMixin, UpdateView):
    model = GroupMember
    form_class = GroupMemberForm
    template_name = 'groups/group-member-change-role.html'
    staff_roles = (RoleChoices.ADMIN,)

    def get_group(self):
        return get_object_or_404(Group, slug=self.kwargs['slug'])

    def test_func(self):
        return self.user_is_group_staff(self.get_group(), self.request.user)

    def get_queryset(self):
        return GroupMember.objects.filter(group=self.get_group()).select_related('group', 'user')

    def form_valid(self, form):
        target_member = self.get_object()

        if target_member.user == target_member.group.owner:
            return self.handle_no_permission()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('group-details', kwargs={'slug': self.kwargs['slug']}) + '?tab=members'

class GroupMemberDeleteView(LoginRequiredMixin, GroupAccessMixin, UserPassesTestMixin, DeleteView):
    model = GroupMember
    staff_roles = (RoleChoices.ADMIN,)

    def get_group(self):
        return get_object_or_404(Group, slug=self.kwargs['slug'])

    def test_func(self):
        return self.user_is_group_staff(self.get_group(), self.request.user)

    def get_queryset(self):
        return GroupMember.objects.filter(group=self.get_group()).select_related('group', 'user')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.user == self.object.group.owner:
            return self.handle_no_permission()

        group = self.object.group
        user = self.object.user

        submitted_artworks = list(
            group.artworks.filter(
                group_submissions__group=group,
                group_submissions__submitted_by=user,
                group_submissions__status=StatusChoices.APPROVED,
            ).distinct()
        )
        for folder in group.folders.filter(artworks__in=submitted_artworks).distinct():
            folder.artworks.remove(*submitted_artworks)

        group.artworks.remove(*submitted_artworks)

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('group-details', kwargs={'slug': self.kwargs['slug']}) + '?tab=members'
