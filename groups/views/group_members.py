from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from groups.models import Group, GroupMember


class ToggleGroupMembershipView(LoginRequiredMixin, View):
    def post(self, request, slug, *args, **kwargs):
        group = get_object_or_404(Group, slug=slug)
        membership = GroupMember.objects.filter(group=group, user=request.user).first()

        if membership:
            membership.delete()
        else:
            GroupMember.objects.create(group=group, user=request.user)

        return redirect('group-details', slug=slug)