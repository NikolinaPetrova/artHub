from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from groups.forms.post import PostCreateForm, PostUpdateForm
from groups.models import Post, Group
from interactions.forms import CreateCommentForm, ReplyForm, CommentEditForm
from notifications.services import NotificationService


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'groups/post-form.html'

    def get_group(self):
        return get_object_or_404(Group, slug=self.kwargs['slug'])

    def test_func(self):
        group = self.get_group()
        return group.members.filter(user=self.request.user).exists()

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, "You must be a member of this group to create a post.")
            return redirect('group-details', slug=self.kwargs['slug'])
        return super().handle_no_permission()

    def form_valid(self, form):
        form.instance.group = self.get_group()
        form.instance.author = self.request.user
        response = super().form_valid(form)
        NotificationService.notify_new_post(self.object)
        return response

    def get_success_url(self):
        return reverse_lazy('group-details', kwargs={'slug': self.kwargs['slug']}) + "?tab=posts"

class PostDetailsView(DetailView):
    model = Post
    template_name = 'groups/post-details.html'
    context_object_name = 'post'

    def get_queryset(self):
        group_slug = self.kwargs.get('slug')
        post_pk = self.kwargs.get('pk')
        return (Post.objects.filter(group__slug=group_slug, pk=post_pk)
        .select_related('author', 'group')
        .prefetch_related(
            'likes',
            'comments',
            'comments__user',
            'comments__child_replies',
            'comments__child_replies__user',
            'comments__likes',
            'comments__child_replies__likes',
        ))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        user = self.request.user

        context['comment_form'] = CreateCommentForm()
        context['reply_form'] = ReplyForm(initial={'post': post.pk})
        context['edit_form'] = CommentEditForm()
        context['user_like'] = post.likes.filter(user=user).exists() if user.is_authenticated else False
        context['comments'] = post.comments.filter(parent__isnull=True)

        return context

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name = 'groups/post-form.html'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user or self.request.user == post.group.owner

    def get_success_url(self):
        post = self.get_object()
        return reverse('post-details', kwargs={'slug': post.group.slug, 'pk': post.pk})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user or self.request.user == post.group.owner

    def get_success_url(self):
        return reverse_lazy('group-details', kwargs={'slug': self.kwargs['slug']})



