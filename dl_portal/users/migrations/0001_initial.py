# Generated by Django 3.2.8 on 2021-10-30 11:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.TextField(db_index=True, max_length=64, unique=True, verbose_name='Имя пользователя')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('password', models.TextField(verbose_name='Пароль')),
                ('nickname', models.TextField(blank=True, db_index=True, max_length=64, unique=True, verbose_name='Никнейм')),
                ('is_active', models.BooleanField(default=True, verbose_name='Аккаунт активен')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Имеет доступ к админ-панели')),
                ('is_superadmin', models.BooleanField(default=False, verbose_name='Ключевой администратор')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='Дата последнего входа')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Аватар')),
                ('banner', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Баннер профиля')),
                ('info', models.TextField(blank=True, null=True, verbose_name='Сведения о пользователе')),
            ],
            options={
                'verbose_name': 'пользователь',
                'verbose_name_plural': 'пользователи',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='LoreGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(db_index=True, max_length=64, unique=True, verbose_name='Название группы')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание группы')),
                ('permissions', models.ManyToManyField(blank=True, related_name='lore_groups', to='auth.Permission', verbose_name='Права группы')),
            ],
            options={
                'verbose_name': 'лорная группа',
                'verbose_name_plural': 'лорные группы',
                'ordering': ['pk'],
            },
            managers=[
                ('objects', users.models.LoreGroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(db_index=True, max_length=64, unique=True, verbose_name='Название группы')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание группы')),
                ('permissions', models.ManyToManyField(blank=True, related_name='groups', to='auth.Permission', verbose_name='Права группы')),
            ],
            options={
                'verbose_name': 'группа',
                'verbose_name_plural': 'группы',
                'ordering': ['pk'],
            },
            managers=[
                ('objects', users.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.BooleanField(blank=True, null=True, verbose_name='Оценка')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='grades', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'тип оценка',
                'verbose_name_plural': 'типы оценки',
                'ordering': ['pk'],
            },
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_name='users', to='users.Group', verbose_name='Группы прав'),
        ),
        migrations.AddField(
            model_name='user',
            name='lore_groups',
            field=models.ManyToManyField(related_name='users', to='users.LoreGroup', verbose_name='Лороведение'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddConstraint(
            model_name='grade',
            constraint=models.UniqueConstraint(fields=('user', 'value'), name='unique_grade_type'),
        ),
    ]