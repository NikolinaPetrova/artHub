from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from groups.choices import StatusChoices
from groups.mixins import GroupAccessMixin
from groups.models import GroupJoinRequest, GroupMember
from notifications.services import NotificationService


class JoinRequestModerationView(LoginRequiredMixin, GroupAccessMixin, UserPassesTestMixin, View):
    def get_join_request(self):
        return get_object_or_404(GroupJoinRequest, pk=self.kwargs['pk'])

    def test_func(self):
        join_request = self.get_join_request()
        return self.user_is_group_staff(join_request.group, self.request.user)

    def post(self, request, *args, **kwargs):
        join_request = self.get_join_request()

        if join_request.status != StatusChoices.PENDING:
            return redirect(self.get_success_url(join_request))

        action = request.POST.get('action')

        if action not in ['approve', 'reject']:
            return redirect(self.get_success_url(join_request))

        join_request.reviewed_by = self.request.user

        if action == 'approve':
            join_request.status = 'approved'
            GroupMember.objects.create(
                user=join_request.user,
                group=join_request.group
            )
            join_request.delete()
            NotificationService.notify_join_approved(
                join_request.group.owner,
                join_request.group,
                join_request.user
            )

        elif action == 'reject':
            join_request.status = 'rejected'
            join_request.save()
            NotificationService.notify_join_rejected(
                join_request.group.owner,
                join_request.group,
                join_request.user
            )

        return redirect(self.get_success_url(join_request))

    def get_success_url(self, join_request):
        return reverse_lazy('group-details', kwargs={'slug': join_request.group.slug}) + '?tab=members'