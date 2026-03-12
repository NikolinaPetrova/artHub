from django import forms
from django.core.exceptions import ValidationError
from groups.models import Group, GroupSubmission, GroupFolder


class BaseGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = ['owner', 'slug']

    def clean_name(self):
        if Group.objects.filter(name=self.cleaned_data['name']).exists():
            raise ValidationError('A group with this name already exists')
        return self.cleaned_data['name']


class CreateGroupForm(BaseGroupForm):
    ...

class EditGroupForm(BaseGroupForm):
    ...


class GroupSubmissionForm(forms.ModelForm):
    class Meta:
        model = GroupSubmission
        fields = ['artwork', 'folder']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.group = kwargs.pop('group')
        super().__init__(*args, **kwargs)
        self.fields['artwork'].queryset = self.user.artworks.all()
        self.fields['folder'].queryset = self.group.folders.all()

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

