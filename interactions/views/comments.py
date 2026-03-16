from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from artworks.models import Artwork
from groups.models import Post
from interactions.forms.comment_form import CommentEditForm, CreateCommentForm, ReplyForm
from interactions.models import Comment


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
        form = CreateCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user

            if model_type == 'artwork':
                comment.artwork = obj
            elif model_type == 'post':
                comment.post = obj

            comment.save()

        return redirect(request.META.get('HTTP_REFERER'))

class ReplyCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        parent = get_object_or_404(Comment, pk=pk)
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.parent = parent
            reply.artwork = parent.artwork
            reply.post = parent.post
            reply.save()

        return redirect(request.META.get('HTTP_REFERER'))

class CommentEditView(View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)

        if comment.user != request.user:
            return HttpResponseForbidden('You cannot edit this comment.')

        form = CommentEditForm(request.POST, instance=comment)

        if form.is_valid():
            form.save()

        return redirect('artwork-details', pk=comment.artwork.pk)

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    artwork_owner = comment.artwork.user

    if comment.user != request.user and artwork_owner != request.user:
        return HttpResponseForbidden('You cannot delete this comment.')

    if request.method == 'POST':
        comment.delete()

    return redirect('artwork-details', pk=comment.artwork.pk)