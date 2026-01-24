from django import forms
from artworks.models import Comment


class BaseCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'placeholder': 'Add a comment...',
            }),
        }

class CreateCommentForm(BaseCommentForm):
    ...

class CommentEditForm(BaseCommentForm):
    class Meta(BaseCommentForm.Meta):
        widgets = {
            'content': forms.TextInput(
                attrs={'class': 'comment-input'}
            )
        }