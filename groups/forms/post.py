from django import forms

from groups.models import Post


class BasePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'content': forms.Textarea(attrs={'placeholder': 'Content'}),
        }

        labels = {
            'title': '',
            'content': '',
        }

class PostCreateForm(BasePostForm):
    ...

class PostUpdateForm(BasePostForm):
    ...