from django import forms
from django.core.exceptions import ValidationError
import re

from .utils import LabelSuffixMixin
from .models import Post


class PostForm(LabelSuffixMixin, forms.ModelForm):
    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'[^\d\w\sА-Яа-я-–—.,()/…?:$%&#@*!№+=_]', title):
            raise ValidationError('Использованы запрещённые символы')
        return title

    class Meta:
        model = Post
        # fields = '__all__'  # Не рекомендуется, получает все поля формы
        fields = ['title', 'content', 'author', 'category']

        widgets = {
            'title': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Заголовок поста",
            }),
            'content': forms.Textarea(attrs={
                "class": "form-control",
                "rows": "15",
            }),
            'author': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Автор",
            }),
            'category': forms.Select(attrs={
                "class": "form-select",
            }),
        }

        labels = {
            'title': "Заголовок",
            'content': "Текст",
            'author': "Автор",
            'category': "Категория",
        }
