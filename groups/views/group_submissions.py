from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from groups.choices import RoleChoices
from groups.forms import GroupSubmissionForm
from groups.models import Group, GroupSubmission
from notifications.services import NotificationService


class GroupArtworkSubmitView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = GroupSubmission
    form_class = GroupSubmissionForm
    template_name = 'groups/group_artwork_submit.html'
    context_object_name = 'submission'

    def dispatch(self, request, *args, **kwargs):
        self.group = get_object_or_404(Group, slug=self.kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.group.members.filter(user=self.request.user).exists()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['group'] = self.group
        return kwargs

    def form_valid(self, form):
        submission = form.save(commit=False)
        submission.group = self.group
        submission.submitted_by = self.request.user

        membership = self.group.members.filter(user=self.request.user).first()

        is_admin_or_moderator = (
                self.request.user == self.group.owner or
                (membership and membership.role in [RoleChoices.ADMIN, RoleChoices.MODERATOR])
        )

        if is_admin_or_moderator:
            submission.status = 'approved'
            submission.group.artworks.add(submission.artwork)
            submission.reviewed_by = self.request.user
            if submission.folder:
                submission.folder.artworks.add(submission.artwork)
        else:
            submission.status = 'pending'
            NotificationService.notify_submission(submission.submitted_by, submission.group, submission.artwork)

        submission.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('group-details', kwargs={'slug': self.group.slug})

class SubmissionModerationView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        submission = get_object_or_404(GroupSubmission, pk=self.kwargs['pk'])
        group = submission.group
        membership = group.members.filter(user=self.request.user).first()
        is_admin_or_moderator = (
                self.request.user == group.owner or
                (membership and membership.role in [RoleChoices.ADMIN, RoleChoices.MODERATOR])
        )
        return is_admin_or_moderator

    def post(self, request, *args, **kwargs):
        submission = get_object_or_404(GroupSubmission, pk=self.kwargs['pk'])
        action = request.POST.get('action')

        if action == 'approve':
            submission.status = 'approved'
            submission.group.artworks.add(submission.artwork)
            submission.reviewed_by = self.request.user

            if submission.folder:
                submission.folder.artworks.add(submission.artwork)

            NotificationService.notify_submission_approved(
                submission.reviewed_by,
                submission.group,
                submission.submitted_by,
                submission.artwork,
            )

        elif action == 'reject':
            submission.status = 'rejected'
            submission.reviewed_by = self.request.user

            NotificationService.notify_submission_rejected(
                submission.reviewed_by,
                submission.group,
                submission.submitted_by,
                submission.artwork,
            )

        submission.save()
        return redirect(request.META.get('HTTP_REFERER'))