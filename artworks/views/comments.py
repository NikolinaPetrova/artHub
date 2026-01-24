from django.shortcuts import get_object_or_404, redirect
from django.views import View
from artworks.forms import CommentEditForm
from artworks.models import Comment


def delete_comment(request, pk):
    if request.method == "POST":
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()

    return redirect('artwork-details', pk=comment.artwork.pk)


class CommentEditView(View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        form = CommentEditForm(request.POST, instance=comment)

        if form.is_valid():
            form.save()

        return redirect('artwork-details', pk=comment.artwork.pk)