from django import forms
from albums.models import Album


class BaseAlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['name',]
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Create album',
                }
            )
        }

        labels = {
            'name': '',
        }

class AlbumCreateForm(BaseAlbumForm):
    ...

class AlbumEditForm(BaseAlbumForm):
    ...