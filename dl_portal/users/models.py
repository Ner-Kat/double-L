from django.db import models
from django.db.models import Q
from django.urls import reverse_lazy
from django.conf import settings

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission

from .utils import avatars_upload_path, banners_upload_path


class GroupManager(models.Manager):
    """
    Менеджер групп.
    """
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)


class Group(models.Model):
    """
    Модель пользовательской группы.
    Группа инкапсулирует набор прав и/или статус пользователя на портале.
    """
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
    """
    Менеджер лорных групп.
    """
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)


class LoreGroup(models.Model):
    """
    Модель лорной группы.
    Лорная группа инкапсулирует набор прав и статус пользователя в области определённой вселенной.
    """
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
    """
    Менеджер пользователей.
    """
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

        # Установка username в качестве никнейма:
        # Если username доступен для регистрации, такого же никнейма также быть не должно
        if 'nickname' not in extra_fields or not extra_fields['nickname']:
            user.nickname = username

        user.save()

        return user

    def create_superuser(self, username, password):
        email = 'admin@dl-portal.com'  # E-mail-заглушка для ключевого администратора

        user = self.create_user(username, email, password)
        user.is_admin = True
        user.is_superadmin = True
        user.save()

        return user

    def is_allowed_username(self, username):
        """
        Проверяет, является ли username доступным для регистрации.
        Проверка осуществляется как по username-ам, так и по nickname-ам.
        """
        ex_num = super().get_queryset().filter(Q(username__exact=username) | Q(nickname__exact=username)).count()
        return ex_num == 0


class User(AbstractBaseUser, PermissionsMixin):
    """
    Модель пользователя.
    Включает в себя все основные данные о пользователе, его группы и права,
    а также методы доступа и проверок.
    """
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
    avatar = models.ImageField(verbose_name='Аватар', upload_to=avatars_upload_path, blank=True, null=True)
    lore_groups = models.ManyToManyField(verbose_name='Лороведение', to=LoreGroup,
                                         related_name='users')
    banner = models.ImageField(verbose_name='Баннер профиля', upload_to=banners_upload_path, blank=True, null=True)
    info = models.TextField(verbose_name='Сведения о пользователе', blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    # ----------------------------
    # User properties and addition fields

    def get_groups_list(self):
        return [group for group in self.groups.all()]

    def get_lore_groups_list(self):
        return [lgroup for lgroup in self.lore_groups.all()]

    def get_groups_names_list(self):
        return [group.name for group in self.groups.all()]

    def get_lore_groups_names_list(self):
        return [lgroup.name for lgroup in self.lore_groups.all()]

    # ----------------------------
    # User model utility functions

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse_lazy('userprofile', kwargs={"username": self.username})

    # Является ключевым администратором: override стандартного свойства
    @property
    def is_superuser(self):
        return self.is_superadmin

    # Имеет доступ в админ-панель: override стандартного свойства
    @property
    def is_staff(self):
        return self.is_admin

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    # -----------
    # Permissions

    def has_perm(self, perm, obj=None):
        if self.is_superadmin:
            return True

        if perm in self.get_summary_permissions():
            return True

        return False

    # Список прав, полученных из всех групп пользователя
    def get_groups_permissions(self):
        all_perm = []
        for group in self.groups.all():
            for perm in group.permissions.all():
                all_perm.append(perm.codename)
        return all_perm

    # Список прав, полученных из всех лорных групп пользователя
    def get_lore_groups_permissions(self):
        all_perm = []
        for lgroup in self.lore_groups.all():
            for perm in lgroup.permissions.all():
                all_perm.append(perm.codename)
        return all_perm

    # Список персонально назначенных прав пользователя
    def get_personal_permissions(self):
        all_perm = []
        for perm in self.user_permissions.all():
            all_perm.append(perm.codename)
        return all_perm

    # Список всех имеющихся прав пользователя (из всех источников)
    def get_summary_permissions(self):
        all_perm = [
            *self.get_groups_permissions(),
            *self.get_lore_groups_permissions(),
            *self.get_personal_permissions()
        ]
        return list(set(all_perm))

    # -------------
    # Grades system

    # Получить объект Grade с соответствующим значением оценки (положительное - True)
    def grade(self, value):
        return Grade.objects.get_or_create(user=self, value=value)[0]

    # Получить объект Grade с положительным значением оценки
    def grade_plus(self):
        return Grade.objects.get_or_create(user=self, value=True)[0]

    # Получить объект Grade с отрицательным значением оценки
    def grade_minus(self):
        return Grade.objects.get_or_create(user=self, value=False)[0]

    # ----------
    # Meta class

    class Meta:
        ordering = ['pk']

        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Grade(models.Model):
    """
    Модель пользовательской оценки.
    Предполагает создание двух объектов модели для каждого пользователя:
    положительной и отрицательной оценки.
    Все модули, использующие систему пользовательских оценок, ссылаются на эти объекты.
    """
    user = models.ForeignKey(verbose_name='Пользователь', to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                             related_name='grades')
    value = models.BooleanField(verbose_name='Оценка', blank=True, null=True)

    class Meta:
        ordering = ['pk']

        verbose_name = 'тип оценки'
        verbose_name_plural = 'типы оценки'

        # Для каждого пользователя содержится только два объекта: положительная и отрицательная оценка
        constraints = [
            models.UniqueConstraint(fields=['user', 'value'], name='unique_grade_type'),
        ]
