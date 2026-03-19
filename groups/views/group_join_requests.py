from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from groups.models import GroupJoinRequest, GroupMember
from notifications.services import NotificationService


class JoinRequestModerationView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        join_request = get_object_or_404(GroupJoinRequest, pk=self.kwargs['pk'])
        return self.request.user.is_staff or self.request.user == join_request.group.owner

    def post(self, request, *args, **kwargs):
        join_request = get_object_or_404(GroupJoinRequest, pk=self.kwargs['pk'])

        if join_request.status != 'pending':
            return redirect(request.META.get('HTTP_REFERER'))

        action = request.POST.get('action')

        if action == 'approve':
            join_request.status = 'approved'
            GroupMember.objects.create(
                user=join_request.user,
                group=join_request.group
            )
            join_request.reviewed_by = self.request.user
            join_request.delete()
            NotificationService.notify_join_approved(
                join_request.group.owner,
                join_request.group,
                join_request.user
            )

        elif action == 'reject':
            join_request.status = 'rejected'
            join_request.reviewed_by = self.request.user
            join_request.save()
            NotificationService.notify_join_rejected(
                join_request.group.owner,
                join_request.group,
                join_request.user
            )

        return redirect(request.META.get('HTTP_REFERER'))