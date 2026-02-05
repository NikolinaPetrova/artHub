from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

UserModel = get_user_model()

class ArtHubUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    professional_artist = forms.BooleanField(
        required=False,
        help_text='Are you a professional artist?'
    )
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = (
            'username',
            'password1',
            'password2',
            'email',
            'first_name',
            'last_name',
            'professional_artist'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})


class BaseArtHubUserForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'email', 'professional_artist']


class ArtHubUserUpdateForm(BaseArtHubUserForm):
    ...


class DeleteArtHubUserForm(BaseArtHubUserForm):
    ...