from django.contrib.auth import get_user_model, logout, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from accounts.forms import ArtHubUserCreationForm, ArtHubUserUpdateForm
from accounts.tasks import send_welcome_email
from albums.forms import AlbumCreateForm
from common.permissions import can_manage_user
from groups.models import Group

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
        response = super().form_valid(form)

        if response.status_code in [301, 302]:
            login(self.request, self.object)

        send_welcome_email.delay(self.object.email, self.object.username)

        return response


class UserDetailView(DetailView):
    model = UserModel
    template_name = 'profile/profile-details.html'
    context_object_name = 'user'

    def get_queryset(self):
        return UserModel.objects.prefetch_related(
            'albums',
            'artworks',
            'owned_groups',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        target_user = self.object

        context['can_delete'] = can_manage_user(current_user, target_user, 'accounts.delete_arthubuser')
        context['album_list'] = target_user.albums.all()
        context['album_form'] = AlbumCreateForm()
        context['artwork_list'] = target_user.artworks.all()
        context['group_list'] = target_user.owned_groups.all()
        context['group_member'] = Group.objects.filter(
            members__user=target_user
        ).exclude(owner=target_user).distinct()

        return context

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = UserModel
    form_class = ArtHubUserUpdateForm
    template_name = 'profile/edit-profile.html'

    def get_object(self):
        return self.request.user

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('pk') != request.user.pk:
            return redirect('profile-details', pk=request.user.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.object.pk})

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserModel
    template_name = 'profile/delete-profile.html'

    def test_func(self):
        return can_manage_user(
            self.request.user,
            self.get_object(),
            'accounts.delete_arthubuser',
        )

    def handle_no_permission(self):
        return redirect('home')

    def post(self, request, *args, **kwargs):
        choice = request.POST.get('confirm')
        user = self.get_object()

        if choice == 'yes':
            logout(request) if request.user == user else None
            user.delete()
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            return HttpResponseRedirect(reverse_lazy('profile-details', kwargs={'pk': user.pk}))