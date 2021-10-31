from django.db import models
from django.urls import reverse_lazy
from django.conf import settings

from .utils import preview_upload_path


class Category(models.Model):
    slug = models.SlugField(verbose_name='Slug-имя', max_length=255, unique=True, db_index=True)
    name = models.TextField(verbose_name='Название категории', max_length=64, unique=True, db_index=True)
    description = models.TextField(verbose_name='Описание вселенной', max_length=2048, blank=True, null=True)
    parent = models.ForeignKey(verbose_name='Надкатегория', to='self', on_delete=models.PROTECT,
                               related_name='children', blank=True, null=True)
    universe = models.ForeignKey(verbose_name='Вселенная', to='universes.Universe', on_delete=models.PROTECT,
                                 related_name='categories', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('category', kwargs={"category_slug": self.slug})

    class Meta:
        ordering = ['pk']

        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Post(models.Model):
    slug = models.SlugField(verbose_name='Slug-имя', max_length=255, unique=True, db_index=True, default=None)
    title = models.TextField(verbose_name='Заголовок материала', max_length=256, db_index=True)
    author = models.ForeignKey(verbose_name='Автор', to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                               related_name='posts', blank=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
    category = models.ForeignKey(verbose_name='Категория', to=Category, on_delete=models.PROTECT,
                                 related_name='posts')
    content = models.TextField(verbose_name='Содержание материала')
    short_content = models.TextField(verbose_name='Сокращённый материал', max_length=3072)
    source = models.URLField(verbose_name='Источник', blank=True, null=True)
    views = models.IntegerField(verbose_name='Просмотры', blank=True, default=0)
    rating = models.IntegerField(verbose_name='Рейтинг', blank=True, default=0)
    grades = models.ManyToManyField(verbose_name='Оценки', to='users.Grade', blank=True,
                                    related_name='graduated_posts')
    preview_banner = models.ImageField(verbose_name='Превью', upload_to=preview_upload_path, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('post', kwargs={"post_slug": self.slug})

    def add_grade(self, user, value):
        existing_grade = self.grades.filter(user__exact=user)
        if existing_grade.count() != 0:
            self.grades.remove(existing_grade[0])

        self.grades.add(user.grade(value))

    class Meta:
        ordering = ['-created_at']

        verbose_name = 'материал'
        verbose_name_plural = 'материалы'
