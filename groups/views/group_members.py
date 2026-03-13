from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView, DeleteView
from groups.choices import RoleChoices, JoinPolicy, StatusChoices
from groups.forms import GroupMemberForm
from groups.models import Group, GroupMember, GroupJoinRequest


class ToggleGroupMembershipView(LoginRequiredMixin, View):
    def post(self, request, slug, *args, **kwargs):
        group = get_object_or_404(Group, slug=slug)
        membership = GroupMember.objects.filter(group=group, user=request.user).first()

        if membership:
            membership.delete()
            messages.success(request, "You have left the group.")
        else:
            if group.join_policy == JoinPolicy.APPROVAL:
                if GroupJoinRequest.objects.filter(group=group, user=request.user, status=StatusChoices.REJECTED).exists():
                    messages.error(request, 'You have been rejected from joining the group.')
                else:
                    GroupJoinRequest.objects.create(group=group, user=request.user)
            else:
                GroupMember.objects.create(group=group, user=request.user)

        return redirect('group-details', slug=slug)

class ChangeMemberRoleView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = GroupMember
    form_class = GroupMemberForm
    template_name = 'groups/group-member-change-role.html'

    def test_func(self):
        group = get_object_or_404(Group, slug=self.kwargs['slug'])
        membership = get_object_or_404(
            GroupMember,
            user=self.request.user,
            group=group
        )

        return membership.role == RoleChoices.ADMIN or membership.role == RoleChoices.MODERATOR

    def get_success_url(self):
        return reverse_lazy('group-details', kwargs={'slug': self.kwargs['slug']}) + '?tab=members'

class GroupMembersListView(ListView):
    model = GroupMember
    template_name = 'groups/tabs/group_members-list.html'

class GroupMemberDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = GroupMember

    def test_func(self):
        group = get_object_or_404(Group, slug=self.kwargs['slug'])
        membership = get_object_or_404(
            GroupMember,
            user=self.request.user,
            group=group
        )

        return membership.role == RoleChoices.ADMIN or membership.role == RoleChoices.MODERATOR

    def get_success_url(self):
        return reverse_lazy('group-details', kwargs={'slug': self.kwargs['slug']}) + '?tab=members'
