import requests
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile
from cloudinary.forms import CloudinaryFileField


def data(request):
    username = request.user.username
    return username


class CreateUser(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': 'This is your identification value so it must be unique'
        }

    def __init__(self, *args, **kwargs):
        super(CreateUser, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


class UserProfilePage(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['Nick_Name', 'Profile_pic']
        help_texts = {
            'Nick_Name': 'This will act as your display name',
        }

    def __init__(self, *args, **kwargs):
        super(UserProfilePage, self).__init__(*args, **kwargs)

        self.fields['Nick_Name'].widget.attrs['class'] = 'form-control'
        self.fields['Profile_pic'].widget.attrs['onchange'] = 'profile(event)'
        self.fields['Profile_pic'].widget.attrs['class'] = 'form-control'

    Profile_pic = CloudinaryFileField(
        options={
            'folder': 'Profile/',
            'overwrite': True,
            'resource_type': 'image',
            'invalidate': True,
        })


class UserEdit(UserChangeForm):
    class Meta:
        model = User
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(UserEdit, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['class'] = 'form-control'


class UserProfileEdit(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['Nick_Name', 'Profile_pic']
        help_texts = {
            'Nick_Name': 'This will act as your display name',
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileEdit, self).__init__(*args, **kwargs)

        self.fields['Nick_Name'].widget.attrs['class'] = 'form-control'
        self.fields['Profile_pic'].widget.attrs['onchange'] = 'edit(event)'
        self.fields['Profile_pic'].widget.attrs['class'] = 'form-control'


class VerifyUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1']

    def __init__(self, *args, **kwargs):
        super(VerifyUser, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'

        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
