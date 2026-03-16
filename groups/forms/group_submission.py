from django import forms
from groups.models import GroupSubmission


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
