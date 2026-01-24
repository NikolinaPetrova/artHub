from django import forms
from artworks.models import Reply


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'placeholder': 'Reply to a comment...',
            }),
        }