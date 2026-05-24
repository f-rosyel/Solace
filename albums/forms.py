from django import forms
from .models import Album, Photo


class AlbumForm(forms.ModelForm):
    class Meta:
        model  = Album
        fields = ['title', 'description', 'visibility']
        widgets = {
            'title':       forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Album title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'visibility':  forms.Select(attrs={'class': 'form-control'}),
        }


class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model  = Photo
        fields = ['image', 'caption', 'taken_at']
        widgets = {
            'image':    forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'caption':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Caption (optional)'}),
            'taken_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class PhotoEditForm(forms.ModelForm):
    class Meta:
        model  = Photo
        fields = ['caption', 'taken_at']
        widgets = {
            'caption':  forms.TextInput(attrs={'class': 'form-control'}),
            'taken_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }