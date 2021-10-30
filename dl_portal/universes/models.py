from django.db import models


class Universe(models.Model):
    slug = models.SlugField(verbose_name='Slug-имя', max_length=255, unique=True, db_index=True)
    name = models.TextField(verbose_name='Название вселенной', max_length=64, unique=True, db_index=True)
    description = models.TextField(verbose_name='Описание вселенной', blank=True, null=True)
    short_description = models.TextField(verbose_name='Краткое описание вселенной',
                                         max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

        verbose_name = 'вселенная'
        verbose_name_plural = 'вселенные'
