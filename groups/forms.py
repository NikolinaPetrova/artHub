from django import forms
from groups.models import Group, GroupSubmission


class BaseGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = ['owner', 'slug']

class CreateGroupForm(BaseGroupForm):
    ...

class EditGroupForm(BaseGroupForm):
    ...


class GroupSubmissionForm(forms.ModelForm):
    class Meta:
        model = GroupSubmission
        fields = ['artwork', 'folder']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['artwork'].queryset = user.artworks.all()