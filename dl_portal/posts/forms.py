from django import forms
from django.core.exceptions import ValidationError
import re

from .utils import LabelSuffixMixin
from .models import Post


class PostAddForm(LabelSuffixMixin, forms.ModelForm):
    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'[^\d\w\sА-Яа-я-–—.,()/…?:$%&#@*!№+=_]', title):
            raise ValidationError('Использованы запрещённые символы')
        return title

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'short_content', 'preview_banner']

        widgets = {
            'title': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Заголовок поста",
            }),
            'content': forms.Textarea(attrs={
                "class": "form-control",
                "rows": "15",
            }),
            'category': forms.Select(attrs={
                "class": "form-select",
            }),
            'short_content': forms.Textarea(attrs={
                "class": "form-control",
                "rows": "10",
            }),
            'preview_banner': forms.FileInput(attrs={
                "class": "form-control",
            }),
        }

        labels = {
            'title': "Заголовок",
            'content': "Текст",
            'category': "Категория",
            'short_content': 'Сокращённый текст',
            'preview_banner': 'Превью-баннер',
        }
