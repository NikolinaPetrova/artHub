from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from groups.forms.post import PostCreateForm
from groups.models import Post, Group


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'groups/post-form.html'

    def get_group(self):
        return get_object_or_404(Group, slug=self.kwargs['slug'])

    def test_func(self):
        group = self.get_group()
        return group.members.filter(pk=self.request.user.pk).exists()

    def form_valid(self, form):
        form.instance.group = self.get_group()
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('group-details', kwargs={'slug': self.kwargs['slug']}) + "?tab=posts"