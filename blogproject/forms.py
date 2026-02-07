from django import forms
from .models import Comment
import re

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def clean_text(self):
        t = self.cleaned_data['text']
        if '<' in t or '>' in t or re.search(r'<.*?>', t):
            raise forms.ValidationError("HTML заборонено")
        return t
