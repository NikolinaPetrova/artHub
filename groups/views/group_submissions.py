from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView
from groups.forms import GroupSubmissionForm
from groups.models import Group, GroupSubmission


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
        submission.status = 'pending'
        submission.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('group-details', kwargs={'slug': self.group.slug})


class GroupSubmissionModerationView(UserPassesTestMixin, ListView):
    model = GroupSubmission
    template_name = 'groups/tabs/group_submissions.html'
    context_object_name = 'submissions'

    def test_func(self):
        group = get_object_or_404(Group, slug=self.kwargs['slug'])
        return self.request.user.is_staff or self.request.user == group.owner

    def get_queryset(self):
        group = get_object_or_404(Group, slug=self.kwargs['slug'])
        return group.submissions.filter(status='pending')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = get_object_or_404(Group, slug=self.kwargs['slug'])
        return context

class SubmissionModerationView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        submission = get_object_or_404(GroupSubmission, pk=self.kwargs['pk'])
        return self.request.user.is_staff or self.request.user == submission.group.owner

    def post(self, request, *args, **kwargs):
        submission = get_object_or_404(GroupSubmission, pk=self.kwargs['pk'])
        action = request.POST.get('action')

        if action == 'approve':
            submission.status = 'approved'
            submission.group.artworks.add(submission.artwork)
            submission.reviewed_by = self.request.user

            if submission.folder:
                submission.folder.artworks.add(submission.artwork)

        elif action == 'reject':
            submission.status = 'rejected'
            submission.reviewed_by = self.request.user

        submission.save()
        return redirect(request.META.get('HTTP_REFERER'))