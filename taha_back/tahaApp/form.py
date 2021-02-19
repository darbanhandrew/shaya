from django import forms
from .models import Shop, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = [
            'name',
            'address',
            'logo',
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'name',
            'address'
        ]
