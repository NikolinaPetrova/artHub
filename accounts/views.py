from django.contrib.auth import get_user_model, logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from accounts.forms import ArtHubUserCreationForm, ArtHubUserUpdateForm
from albums.forms import AlbumCreateForm

UserModel = get_user_model()

class RegisterView(CreateView):
    form_class = ArtHubUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            user = form.save()
            login(self.request, user)
        except IntegrityError:
            form.add_error(None, 'This user already exists. Please use another email or username.')
            return self.form_invalid(form)
        return redirect(self.success_url)


class UserDetailView(DetailView):
    model = UserModel
    template_name = 'profile/profile-details.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['album_list'] = self.object.albums.all()
        context['album_form'] = AlbumCreateForm
        context['albums'] = self.object.albums.all()
        return context

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = UserModel
    form_class = ArtHubUserUpdateForm
    template_name = 'profile/edit-profile.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.object.pk})

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = UserModel
    template_name = 'profile/delete-profile.html'

    def post(self, request, *args, **kwargs):
        choice = request.POST.get('confirm')
        user = self.get_object()
        if choice == 'yes':
            logout(request) if request.user == user else None
            user.delete()
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            return HttpResponseRedirect(reverse_lazy('profile-details', kwargs={'pk': self.object.pk}))