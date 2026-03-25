import re
from django import forms
from albums.models import Album
from artworks.models import Artwork, Tag
from common.mixins import DisabledFormFieldsMixin

TAG_REGEX = re.compile(r'^[a-z0-9]+([ -][a-z0-9]+)*$')


class BaseArtworkForm(forms.ModelForm):
    albums = forms.ModelMultipleChoiceField(
        queryset=Album.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    tags = forms.CharField(
        required=False,
        help_text="Enter comma-separated tags (lowercase letters and numbers). Multi-word tags can use a space or a hyphen (-).",
    )

    class Meta:
        model = Artwork
        fields = ['title', 'description', 'image_url', 'type', 'tags']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        artwork_owner = self.instance.user if self.instance.pk else self.user

        if artwork_owner:
            self.fields['albums'].queryset = Album.objects.filter(owner=artwork_owner)

        if self.instance.pk:
            self.fields['albums'].initial = self.instance.albums.filter(owner=artwork_owner)
            self.initial['tags'] = ', '.join(
                tag.name for tag in self.instance.tags.all()
            )

    def clean_tags(self):
        tags_string = self.cleaned_data.get('tags', '')

        if not tags_string:
            return []

        tag_names = [tag.strip().lower() for tag in tags_string.split(',') if tag.strip()]

        for name in tag_names:
            if len(name) > 20:
                raise forms.ValidationError(f'Tag name is too long: "{name}"')
            if not TAG_REGEX.fullmatch(name):
                raise forms.ValidationError(f'Invalid tag: "{name}"')

        return list(set(tag_names))

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        return title

    def save(self, commit=True):
        artwork = super().save(commit=False)

        if self.user and not artwork.pk:
            artwork.user = self.user

        if commit:
            artwork.save()

        tag_names = self.cleaned_data.get('tags', [])
        artwork.tags.clear()

        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            artwork.tags.add(tag)

        if 'albums' in self.cleaned_data:
            artwork.albums.set(self.cleaned_data['albums'])

        return artwork

class CreateArtworkForm(BaseArtworkForm):
    ...

class EditArtworkForm(BaseArtworkForm):
    ...

class DeleteArtworkForm(DisabledFormFieldsMixin, BaseArtworkForm):
    ...