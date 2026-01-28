import re
from django import forms
from artworks.models import Artwork, Tag
from common.mixins import DisabledFormFieldsMixin

TAG_REGEX = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')


class BaseArtworkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['tags'] = ', '.join(
                tag.name for tag in self.instance.tags.all()
            )

    tags = forms.CharField(
        required=False,
        help_text='Enter comma-separated tags',
    )

    class Meta:
        model = Artwork
        fields = ['title', 'description', 'image_url', 'type', 'tags']

    def save(self, commit=True):
        artwork = super().save(commit=False)

        if commit:
            artwork.save()

        tags_string = self.cleaned_data.get('tags', '')
        tag_names = [tag.strip().lower() for tag in tags_string.split(',')]

        artwork.tags.clear()

        for name in tag_names:
            if not TAG_REGEX.fullmatch(name):
                raise forms.ValidationError(f'Invalid tag: "{name}"')
            tag, _ = Tag.objects.get_or_create(name=name)
            artwork.tags.add(tag)

        return artwork

class CreateArtworkForm(BaseArtworkForm):
    ...

class EditArtworkForm(BaseArtworkForm):
    ...

class DeleteArtworkForm(DisabledFormFieldsMixin, BaseArtworkForm):
    ...