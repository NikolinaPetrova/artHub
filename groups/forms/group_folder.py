from django import forms
from groups.models import GroupFolder


class GroupFolderForm(forms.ModelForm):

    class Meta:
        model = GroupFolder
        fields = ['name', 'description']
        labels = {
            'name': '',
            'description': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Folder Name'}),
            'description': forms.Textarea(attrs={
                'placeholder': 'Description',
                'rows': 3,
                'cols': 20,

            }),
        }
