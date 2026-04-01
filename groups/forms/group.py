from django import forms
from django.core.exceptions import ValidationError
from groups.models import Group


class BaseGroupForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    banner = forms.ImageField(required=False)
    class Meta:
        model = Group
        exclude = ['owner', 'slug']


class CreateGroupForm(BaseGroupForm):
    def clean_name(self):
        if Group.objects.filter(name=self.cleaned_data['name']).exists():
            raise ValidationError('A group with this name already exists')
        return self.cleaned_data['name']


class EditGroupForm(BaseGroupForm):
    ...