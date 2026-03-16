from django import forms
from django.core.exceptions import ValidationError
from groups.models import Group


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