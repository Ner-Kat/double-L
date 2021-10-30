# Generated by Django 3.2.8 on 2021-10-30 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Slug-имя')),
                ('name', models.TextField(db_index=True, max_length=64, unique=True, verbose_name='Название категории')),
                ('description', models.TextField(blank=True, max_length=2048, null=True, verbose_name='Описание вселенной')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Slug-имя')),
                ('title', models.TextField(db_index=True, max_length=256, verbose_name='Заголовок материала')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('content', models.TextField(verbose_name='Содержание материала')),
                ('short_content', models.TextField(max_length=3072, verbose_name='Сокращённый материал')),
                ('source', models.URLField(blank=True, null=True, verbose_name='Источник')),
                ('views', models.IntegerField(blank=True, default=0, verbose_name='Просмотры')),
                ('rating', models.IntegerField(blank=True, default=0, verbose_name='Рейтинг')),
                ('preview_banner', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Превью')),
            ],
            options={
                'verbose_name': 'материал',
                'verbose_name_plural': 'материалы',
                'ordering': ['-created_at'],
            },
        ),
    ]
