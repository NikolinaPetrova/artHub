from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from common.utils import get_profile
from profiles.forms import CreateProfileForm, EditProfileForm, ProfileDetailsForm, DeleteProfileForm
from profiles.models import Profile

class ProfileCreateView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'profile/create-profile.html'
    success_url = reverse_lazy('gallery')


class ProfileDetailsView(DetailView):
    model = Profile
    form_class = ProfileDetailsForm
    template_name = 'profile/profile-details.html'

    def get_object(self, queryset=None):
        return get_profile()


class ProfileEditView(UpdateView):
    model = Profile
    form_class = EditProfileForm
    template_name = 'profile/edit-profile.html'
    success_url = reverse_lazy('profile-details')

    def get_object(self, queryset=None):
        return get_profile()


class ProfileDeleteView(DeleteView):
    template_name = 'profile/delete-profile.html'
    form_class = DeleteProfileForm

    def get_object(self, queryset=None):
        return get_profile()

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(instance=self.get_object(), **self.get_form_kwargs())

    def post(self, request, *args, **kwargs):
        choice = request.POST.get('confirm')
        profile = self.get_object()
        if choice == 'yes':
            profile.delete()
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            return HttpResponseRedirect(reverse_lazy('profile-details'))