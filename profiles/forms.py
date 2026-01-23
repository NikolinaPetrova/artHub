from django import forms
from profiles.models import Profile


class BaseProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'First Name',
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Last Name',
                }
            ),

            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Username',
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Email',
                }
            ),

            'age': forms.NumberInput(
                attrs={
                    'placeholder': 'Age',
                }
            ),
        }

class CreateProfileForm(BaseProfileForm):
    ...

class ProfileDetailsForm(BaseProfileForm):
    ...

class EditProfileForm(BaseProfileForm):
    class Meta(BaseProfileForm.Meta):
        exclude = ['professional_artist']

class DeleteProfileForm(BaseProfileForm):
    ...