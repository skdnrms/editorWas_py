from django import forms
from froala_editor.widgets import FroalaEditor
from .models import Post, Page

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'contents',)

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('contents',)