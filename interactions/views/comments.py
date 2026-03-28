from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DeleteView
from artworks.models import Artwork
from groups.models import Post
from interactions.forms.comment_form import CommentEditForm, CreateCommentForm, ReplyForm
from interactions.models import Comment
from groups.utils import is_group_member
from notifications.services import NotificationService


class AddCommentView(LoginRequiredMixin, View):
    MODEL_MAP = {
        'artwork': Artwork,
        'post': Post,
    }

    def post(self, request, model_type, pk):
        model = self.MODEL_MAP.get(model_type)

        if not model:
            return redirect('home')

        obj = get_object_or_404(model, pk=pk)

        if model_type == 'post' and not is_group_member(request.user, obj.group):
            messages.error(request, 'You must be a group member to comment on posts.')
            return redirect('group-details', slug=obj.group.slug)

        form = CreateCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user

            if model_type == 'artwork':
                comment.artwork = obj
            elif model_type == 'post':
                comment.post = obj

            comment.save()
            NotificationService.notify_comment(comment)

        return redirect(request.META.get('HTTP_REFERER'))

class ReplyCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        parent = get_object_or_404(Comment, pk=pk)

        if parent.post and not is_group_member(request.user, parent.post.group):
            messages.error(request, 'You must be a group member to reply to comments.')
            return redirect('group-details', slug=parent.post.group.slug)

        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.parent = parent
            reply.artwork = parent.artwork
            reply.post = parent.post
            reply.save()
            NotificationService.notify_comment(reply)

        return redirect(request.META.get('HTTP_REFERER'))

class CommentEditView(View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)

        if not (
                comment.user == request.user
                or request.user.has_perm('interactions.change_comment')
        ):
            return HttpResponseForbidden('You cannot edit this comment.')

        form = CommentEditForm(request.POST, instance=comment)

        if form.is_valid():
            form.save()

        if comment.artwork:
            return redirect('artwork-details', pk=comment.artwork.pk)
        elif comment.post:
            return redirect('post-details', slug=comment.post.group.slug, pk=comment.post.pk)
        else:
            return redirect('home')

class CommentDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        comment = self.get_object()
        user = self.request.user

        return (
            comment.user == user
            or (comment.artwork and comment.artwork.user == user)
            or (comment.post and comment.post.author == user)
            or user.has_perm('interactions.delete_comment')
        )

    def handle_no_permission(self):
        return redirect('home')

    def get_success_url(self):
        comment = self.object
        if comment.artwork:
            return reverse('artwork-details', kwargs={'pk': comment.artwork.pk})
        elif comment.post:
            return reverse('post-details', kwargs={'slug': comment.post.group.slug, 'pk': comment.post.pk})
        else:
            return reverse('home')
