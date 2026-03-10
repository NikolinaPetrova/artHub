from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, DetailView, FormView, DeleteView
from groups.choices import RoleChoices
from groups.forms import CreateGroupForm, EditGroupForm, GroupSubmissionForm
from groups.models import Group, GroupMember, GroupSubmission


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
        context['members'] = self.object.members.all()
        context['group_artworks'] = self.object.artworks.all()
        context['joined_to_group'] = self.object.members.filter(user=self.request.user.pk).exists()
        return context

class ToggleGroupMembershipView(LoginRequiredMixin, View):
    def post(self, request, slug, *args, **kwargs):
        group = get_object_or_404(Group, slug=slug)
        membership = GroupMember.objects.filter(group=group, user=request.user).first()

        if membership:
            membership.delete()
        else:
            GroupMember.objects.create(group=group, user=request.user)

        return redirect('group-details', slug=slug)

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

class GroupArtworkSubmitView(FormView):
    template_name = 'groups/group_artwork_submit.html'
    form_class = GroupSubmissionForm

    def dispatch(self, request, *args, **kwargs):
        self.group = get_object_or_404(Group, slug=self.kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        submission = form.save(commit=False)
        submission.group = self.group
        submission.submitted_by = self.request.user
        submission.status = 'pending'
        submission.save()
        return redirect('group-details', slug=self.group.slug)


class GroupSubmissionModerationView(UserPassesTestMixin, ListView):
    model = GroupSubmission
    template_name = 'profile/tabs/group_submissions.html'
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
        elif action == 'reject':
            submission.status = 'rejected'

        submission.save()
        return redirect(request.META.get('HTTP_REFERER'))