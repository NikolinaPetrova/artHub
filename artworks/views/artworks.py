from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from artworks.forms import CreateArtworkForm, EditArtworkForm, DeleteArtworkForm
from artworks.models import Artwork
from interactions.forms.comment_form import CreateCommentForm, ReplyForm, CommentEditForm
from interactions.models import Comment


class CreateArtworkView(LoginRequiredMixin, CreateView):
    model = Artwork
    form_class = CreateArtworkForm
    template_name = 'artwork/create-artwork.html'
    success_url = reverse_lazy('gallery')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ArtworkDetailsView(DetailView):
    model = Artwork
    template_name = 'artwork/artwork-details.html'
    context_object_name = 'artwork'

    def get_queryset(self):
        return (
            Artwork.objects
            .select_related('user')
            .prefetch_related(
                'tags',
                'albums',
                'likes',
                'comments__user',
                'comments__child_replies__user',
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artwork = self.object
        user = self.request.user

        context.setdefault('comment_form', CreateCommentForm())
        context.setdefault('reply_form', ReplyForm())
        context.setdefault('edit_form', CommentEditForm())

        context['user_like'] = (
            artwork.likes.filter(user=user).exists()
            if user.is_authenticated else False
        )

        context['comments'] = artwork.comments.filter(parent__isnull=True)
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if 'comment_submit' in request.POST:
            return self.handle_comment()

        if 'reply_submit' in request.POST:
            return self.handle_reply()

        if 'edit_submit' in request.POST:
            return self.handle_edit()

        return redirect('artwork-details', pk=self.object.pk)


    def handle_comment(self):
        form = CreateCommentForm(self.request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = self.request.user
            comment.artwork = self.object
            comment.save()

            return redirect('artwork-details', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(comment_form=form))

    def handle_reply(self):
        form = ReplyForm(self.request.POST)
        parent_id = self.request.POST.get('parent_id')
        parent = get_object_or_404(
            Comment,
            pk=parent_id,
            artwork=self.object,
        )

        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = self.request.user
            reply.artwork = self.object
            reply.parent = parent
            reply.save()

            return redirect('artwork-details', pk=self.object.pk)

        return self.render_to_response(
            self.get_context_data(reply_form=form)
        )

    def handle_edit(self):
        comment_id = self.request.POST.get('comment_id')
        comment = get_object_or_404(
            Comment,
            pk=comment_id,
            artwork=self.object,
            user=self.request.user
        )

        form = CommentEditForm(
            self.request.POST,
            instance=comment,
        )

        if form.is_valid():
            form.save()

        return redirect('artwork-details', pk=self.object.pk)

class EditArtworkView(LoginRequiredMixin, UpdateView):
    model = Artwork
    template_name = 'artwork/edit-artwork.html'
    form_class = EditArtworkForm

    def get_form_kwargs(self, form_class=None):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('artwork-details', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        return Artwork.objects.filter(user=self.request.user)

class DeleteArtworkView(LoginRequiredMixin, DeleteView):
    model = Artwork
    form_class = DeleteArtworkForm
    template_name = 'artwork/delete-artwork.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

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

    def get_queryset(self):
        return Artwork.objects.filter(user=self.request.user)