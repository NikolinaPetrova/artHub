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

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if len(title) < 3:
            raise forms.ValidationError('Title must be at least 3 characters long')
        return title

    def clean_content(self):
        content = self.cleaned_data['content'].strip()
        if not content:
            raise forms.ValidationError('Content cannot be empty')
        return content

class PostCreateForm(BasePostForm):
    ...

class PostUpdateForm(BasePostForm):
    ...