from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from groups.choices import StatusChoices
from groups.forms import GroupSubmissionForm
from groups.mixins import GroupAccessMixin
from groups.models import Group, GroupSubmission
from notifications.services import NotificationService


class GroupArtworkSubmitView(LoginRequiredMixin, GroupAccessMixin, UserPassesTestMixin, CreateView):
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

        is_group_staff = self.user_is_group_staff(self.group, self.request.user)

        if is_group_staff:
            submission.status = StatusChoices.APPROVED
            submission.reviewed_by = self.request.user
        else:
            submission.status = StatusChoices.PENDING

        submission.save()
        self.object = submission

        if is_group_staff:
            submission.group.artworks.add(submission.artwork)

            if submission.folder:
                submission.folder.artworks.add(submission.artwork)
        else:
            NotificationService.notify_submission(
                submission.submitted_by,
                submission.group,
                submission.artwork,
            )

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('group-details', kwargs={'slug': self.group.slug})

class SubmissionModerationView(LoginRequiredMixin, GroupAccessMixin, UserPassesTestMixin, View):
    def get_submission(self):
        return get_object_or_404(GroupSubmission, pk=self.kwargs['pk'])

    def test_func(self):
        submission = self.get_submission()
        return self.user_is_group_staff(submission.group, self.request.user)

    def post(self, request, *args, **kwargs):
        submission = self.get_submission()
        action = request.POST.get('action')

        if submission.status != StatusChoices.PENDING:
            return redirect(self.get_success_url(submission))

        if action not in {'approve', 'reject'}:
            return redirect(self.get_success_url(submission))

        if action == 'approve':
            submission.status = StatusChoices.APPROVED
            submission.reviewed_by = self.request.user
            submission.save()

            submission.group.artworks.add(submission.artwork)

            if submission.folder:
                submission.folder.artworks.add(submission.artwork)

            NotificationService.notify_submission_approved(
                submission.reviewed_by,
                submission.group,
                submission.submitted_by,
                submission.artwork,
            )

        elif action == 'reject':
            submission.status = StatusChoices.REJECTED
            submission.reviewed_by = self.request.user
            submission.save()

            NotificationService.notify_submission_rejected(
                submission.reviewed_by,
                submission.group,
                submission.submitted_by,
                submission.artwork,
            )

        return redirect(self.get_success_url(submission))

    def get_success_url(self, submission):
        return reverse_lazy('group-details', kwargs={'slug': submission.group.slug}) + '?tab=submissions'