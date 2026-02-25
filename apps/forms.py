from django import forms
from .models import Profile, Blog

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'category', 'img_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Blog sarlavhasi'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Blog mazmuni'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'img_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Rasim URL'}),
        }