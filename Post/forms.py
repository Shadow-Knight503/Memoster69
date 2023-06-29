from django import forms
from .models import Meme, Comment, Msg
from django.forms import ModelForm, TextInput
from cloudinary.forms import CloudinaryFileField


class PostMemes(forms.ModelForm):
    class Meta:
        model = Meme
        fields = ['Title', 'Post', 'Type']
        help_texts = {
            'Title': None,
        }

    Post = CloudinaryFileField(
        options={
            'folder': 'Posts/',
            'resource_type': 'auto',
        })

    def __init__(self, *args, **kwargs):
        super(PostMemes, self).__init__(*args, **kwargs)

        self.fields['Title'].widget.attrs['class'] = 'form-control'
        self.fields['Post'].widget.attrs['onchange'] = "Meme(event, this)"


class CommentSection(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        super(CommentSection, self).__init__(*args, **kwargs)

        self.fields['comment'].widget.attrs['class'] = 'form-control'
        self.fields['comment'].widget.attrs['placeholder'] = 'Enter Something here'
        self.fields['comment'].widget.attrs['style'] = 'background-color:black'


class MsgBuild(forms.ModelForm):
    class Meta:
        model = Msg
        fields = ['cnt']

    def __init__(self, *args, **kwargs):
        super(MsgBuild, self).__init__(*args, **kwargs)

        self.fields['cnt'].widget.attrs['class'] = 'form-control'
        self.fields['cnt'].widget.attrs['placeholder'] = 'Enter Something here'
        self.fields['cnt'].widget.attrs['style'] = 'background-color:black'

