from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from artworks.forms import CreateArtworkForm, EditArtworkForm, CreateCommentForm, ReplyForm, CommentEditForm, \
    DeleteArtworkForm
from artworks.models import Artwork, Comment
from common.utils import get_profile


class CreateArtworkView(CreateView):
    model = Artwork
    form_class = CreateArtworkForm
    template_name = 'artwork/create-artwork.html'
    success_url = reverse_lazy('gallery')

    def form_valid(self, form):
        form.instance.profile = get_profile()
        return super().form_valid(form)

class ArtworkDetailsView(DetailView):
    model = Artwork
    template_name = 'artwork/artwork-details.html'
    context_object_name = 'artwork'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artwork = self.get_object()
        profile = get_profile()

        context['has_profile'] = profile
        context['comment_form'] = kwargs.get('comment_form', CreateCommentForm())
        context['reply_form'] = kwargs.get('reply_form', ReplyForm())
        context['edit_form'] = CommentEditForm()
        context['user_like'] = artwork.likes.filter(profile=profile).exists()
        context['comments'] = artwork.comments.prefetch_related('replies')
        return context

    def post(self, request, *args, **kwargs):
        artwork = self.get_object()
        profile = get_profile()

        if 'comment_submit' in request.POST:
            form = CreateCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = profile
                comment.artwork = artwork
                comment.save()
                return redirect('artwork-details', pk=artwork.pk)
            else:
                return self.get_context_data(comment_form=form)

        elif 'reply_submit' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = Comment.objects.get(pk=comment_id)
            form = ReplyForm(request.POST)
            if form.is_valid():
                reply = form.save(commit=False)
                reply.comment = comment
                reply.artwork = artwork
                reply.author = profile
                reply.save()
                return redirect('artwork-details', pk=artwork.pk)
            else:
                return self.get_context_data(reply_form=form)

        return self.render_to_response(self.get_context_data())

class EditArtworkView(UpdateView):
    model = Artwork
    template_name = 'artwork/edit-artwork.html'
    form_class = EditArtworkForm

    def get_success_url(self):
        return reverse('artwork-details', kwargs={'pk': self.object.pk})

class DeleteArtworkView(DeleteView):
    model = Artwork
    form_class = DeleteArtworkForm
    template_name = 'artwork/delete-artwork.html'

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(instance=self.get_object(), **self.get_form_kwargs())

    def post(self, request, *args, **kwargs):
        choice = request.POST.get('confirm')
        artwork = self.get_object()
        if choice == 'yes':
            artwork.delete()
            return HttpResponseRedirect(reverse_lazy('gallery'))
        else:
            return HttpResponseRedirect(reverse_lazy('artwork-details', kwargs={'pk': artwork.pk}))