from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from artworks.models import Artwork
from interactions.forms.comment_form import CommentEditForm, CreateCommentForm, ReplyForm
from interactions.models import Comment

class AddArtworkCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        artwork = get_object_or_404(Artwork, pk=pk)
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.artwork = artwork
            comment.save()
        return redirect('artwork-details', pk=artwork.pk)


class ReplyArtworkCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        parent = get_object_or_404(Comment, pk=pk)
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.artwork = parent.artwork
            reply.parent = parent
            reply.save()
        return redirect('artwork-details', pk=parent.artwork.pk)

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