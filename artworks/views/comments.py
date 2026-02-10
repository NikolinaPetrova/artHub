from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from artworks.forms import CommentEditForm
from artworks.models import Comment


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