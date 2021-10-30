from django.db import models
from django.db.models import Q
from django.urls import reverse_lazy
from django.conf import settings

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission


class GroupManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)


class Group(models.Model):
    name = models.TextField(verbose_name='Название группы', max_length=64, unique=True, db_index=True)
    permissions = models.ManyToManyField(verbose_name='Права группы', to=Permission, blank=True,
                                         related_name='groups')
    description = models.TextField(verbose_name='Описание группы', blank=True, null=True)

    objects = GroupManager()

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name, )

    class Meta:
        ordering = ['pk']

        verbose_name = 'группа'
        verbose_name_plural = 'группы'


class LoreGroupManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)


class LoreGroup(models.Model):
    name = models.TextField(verbose_name='Название группы', max_length=64, unique=True, db_index=True)
    permissions = models.ManyToManyField(verbose_name='Права группы', to=Permission, blank=True,
                                         related_name='lore_groups')
    description = models.TextField(verbose_name='Описание группы', blank=True, null=True)

    objects = LoreGroupManager()

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name, )

    class Meta:
        ordering = ['pk']

        verbose_name = 'лорная группа'
        verbose_name_plural = 'лорные группы'


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        if not username:
            raise TypeError('Отсутствует имя пользователя.')

        if not self.is_allowed_username(username):
            raise ValueError('Данное имя пользователя не может быть зарегистрировано.')

        if not email:
            raise TypeError('Отсутствует e-mail.')

        if not password:
            raise TypeError('Отсутствует пароль.')

        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)

        if 'nickname' not in extra_fields or not extra_fields['nickname']:
            user.nickname = username

        user.save()

        return user

    def create_superuser(self, username, password):
        email = 'admin@dl-portal.com'
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.is_superadmin = True
        user.save()

        return user

    def is_allowed_username(self, username):
        ex_num = super().get_queryset().filter(Q(username__exact=username) | Q(nickname__exact=username)).count()
        return ex_num == 0


class User(AbstractBaseUser, PermissionsMixin):
    username = models.TextField(verbose_name='Имя пользователя', max_length=64, unique=True, db_index=True)
    email = models.EmailField(verbose_name='E-mail', unique=True)
    password = models.TextField(verbose_name='Пароль')
    nickname = models.TextField(verbose_name='Никнейм', max_length=64, unique=True, db_index=True, blank=True)
    is_active = models.BooleanField(verbose_name='Аккаунт активен', default=True)
    is_admin = models.BooleanField(verbose_name='Имеет доступ к админ-панели', default=False)
    is_superadmin = models.BooleanField(verbose_name='Ключевой администратор', default=False)
    date_joined = models.DateTimeField(verbose_name='Дата регистрации', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Дата последнего входа', blank=True, null=True)
    groups = models.ManyToManyField(verbose_name='Группы прав', to=Group,
                                    related_name='users')
    avatar = models.ImageField(verbose_name='Аватар', blank=True, null=True)
    lore_groups = models.ManyToManyField(verbose_name='Лороведение', to=LoreGroup,
                                         related_name='users')
    banner = models.ImageField(verbose_name='Баннер профиля', blank=True, null=True)
    info = models.TextField(verbose_name='Сведения о пользователе', blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.username

    # def get_absolute_url(self):
    #     return reverse_lazy('userinfo', kwargs={"username": self.username})

    @property
    def is_superuser(self):
        return self.is_superadmin

    @property
    def is_staff(self):
        return self.is_admin

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def grade(self, value):
        return Grade.objects.get_or_create(user=self, value=value)[0]

    def grade_plus(self):
        return Grade.objects.get_or_create(user=self, value=True)[0]

    def grade_minus(self):
        return Grade.objects.get_or_create(user=self, value=False)[0]

    class Meta:
        ordering = ['pk']

        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Grade(models.Model):
    user = models.ForeignKey(verbose_name='Пользователь', to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                             related_name='grades')
    value = models.BooleanField(verbose_name='Оценка', blank=True, null=True)

    class Meta:
        ordering = ['pk']

        verbose_name = 'тип оценка'
        verbose_name_plural = 'типы оценки'

        constraints = [
            models.UniqueConstraint(fields=['user', 'value'], name='unique_grade_type'),
        ]
