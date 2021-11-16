from django import forms
from .models import MemeImg


class PostImg(forms.ModelForm):
    class Meta:
        model = MemeImg
        fields = '__all__'
