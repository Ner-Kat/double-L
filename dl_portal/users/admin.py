from django.contrib import admin
from django.contrib.auth.models import Group as DjangoGroup

from .models import User, Group, LoreGroup


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'date_joined', 'is_active', 'is_admin', )
    list_display_links = ('pk', 'username', )
    search_fields = ('username', 'nickname', 'email', 'info', )
    list_editable = ('is_active', 'is_admin', )
    list_filter = ('is_active', 'is_admin', )

    fields = ('pk', 'username', 'email', 'password', 'nickname', 'is_active', 'is_admin', 'is_superadmin',
              'date_joined', 'last_login', 'groups', 'avatar', 'lore_groups', 'banner', 'info', )
    readonly_fields = ('pk', 'date_joined', 'last_login', )

    save_on_top = True


class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', )
    list_display_links = ('pk', 'name', )
    search_fields = ('name', 'description', )
    list_editable = ()
    list_filter = ()

    fields = ('pk', 'name', 'permissions', 'description', )
    readonly_fields = ('pk', )

    save_on_top = True


class LoreGroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', )
    list_display_links = ('pk', 'name', )
    search_fields = ('name', 'description', )
    list_editable = ()
    list_filter = ()

    fields = ('pk', 'name', 'permissions', 'description', )
    readonly_fields = ('pk', )

    save_on_top = True


admin.site.unregister(DjangoGroup)
admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(LoreGroup, LoreGroupAdmin)
