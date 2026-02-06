from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from artworks.forms import CreateArtworkForm, EditArtworkForm, CreateCommentForm, CommentEditForm, DeleteArtworkForm, \
    ReplyForm
from artworks.models import Artwork, Comment


class CreateArtworkView(LoginRequiredMixin, CreateView):
    model = Artwork
    form_class = CreateArtworkForm
    template_name = 'artwork/create-artwork.html'
    success_url = reverse_lazy('gallery')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['albums'].queryset = self.request.user.albums.all()
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        self.object.albums.set(form.cleaned_data['albums'])
        return response


class ArtworkDetailsView(DetailView):
    model = Artwork
    template_name = 'artwork/artwork-details.html'
    context_object_name = 'artwork'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artwork = self.get_object()
        user = self.request.user

        context['comment_form'] = kwargs.get('comment_form', CreateCommentForm())
        context['reply_form'] = kwargs.get('reply_form', ReplyForm())
        context['edit_form'] = CommentEditForm()
        context['user_like'] = artwork.likes.filter(user=user).exists() if user.is_authenticated else False
        context['comments'] = artwork.comments.filter(parent__isnull=True).prefetch_related('child_replies')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        artwork = self.object
        user = request.user

        if not user.is_authenticated:
            return redirect('login')

        if 'comment_submit' in request.POST:
            form = CreateCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = user
                comment.artwork = artwork
                comment.parent = None
                comment.save()
                return redirect('artwork-details', pk=artwork.pk)
            else:
                context = self.get_context_data(comment_form=form)
                return self.render_to_response(context)

        elif 'reply_submit' in request.POST:
            form = ReplyForm(request.POST)
            parent_id = request.POST.get('parent_id')
            parent_reply = get_object_or_404(Comment, pk=parent_id) if parent_id else None

            if form.is_valid():
                reply = form.save(commit=False)
                reply.user = user
                reply.artwork = artwork
                reply.parent = parent_reply
                reply.save()
                return redirect('artwork-details', pk=artwork.pk)
            else:
                context = self.get_context_data(reply_form=form)
                return self.render_to_response(context)

        elif 'edit_submit' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, pk=comment_id)
            form = CommentEditForm(request.POST, instance=comment)

            if form.is_valid():
                form.save()

            return redirect('artwork-details', pk=artwork.pk)

        return self.render_to_response(self.get_context_data())

class EditArtworkView(LoginRequiredMixin, UpdateView):
    model = Artwork
    template_name = 'artwork/edit-artwork.html'
    form_class = EditArtworkForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['albums'].queryset = self.request.user.albums.all()
        form.fields['albums'].initial = self.object.albums.all()
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        selected_albums = form.cleaned_data['albums']
        self.object.albums.set(selected_albums)
        return response

    def get_success_url(self):
        return reverse('artwork-details', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        return Artwork.objects.filter(user=self.request.user)

class DeleteArtworkView(LoginRequiredMixin, DeleteView):
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

    def get_queryset(self):
        return Artwork.objects.filter(user=self.request.user)