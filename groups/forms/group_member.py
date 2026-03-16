from django import forms
from groups.models import GroupMember


class GroupMemberForm(forms.ModelForm):
    class Meta:
        model = GroupMember
        fields = ['role']
