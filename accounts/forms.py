import re
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinLengthValidator
from accounts.models import ArtHubUser

UserModel = get_user_model()
USERNAME_REGEX = r'^[a-z0-9_-]+$'

class ArtHubUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        validators=[MinLengthValidator(3)],
        help_text='Choose a username using lowercase letters, numbers, - or _.'
    )

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
        self.fields['username'].widget.attrs.update({'placeholder': 'Example: john_doe-123'})
        self.fields['password1'].help_text = "Use 8+ characters, avoid using your username or only letters/numbers."

    def clean_username(self):
        username = self.cleaned_data['username'].strip()

        if not re.match(USERNAME_REGEX, username):
            raise forms.ValidationError('Username can contain only lowercase letters, digits, dashes or underscores.')

        if not re.search(r'[a-z0-9]', username):
            raise forms.ValidationError('Username must contain at least one letter or number.')

        if username[0] in '_-' or username[-1] in '_-':
            raise forms.ValidationError('Username cannot start or end with "-" or "_"')
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        if ArtHubUser.objects.filter(email=email).exists():
            raise forms.ValidationError('User with this email already exists.')
        return email


class BaseArtHubUserForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'email', 'professional_artist']


class ArtHubUserUpdateForm(BaseArtHubUserForm):
    ...