from django.contrib import admin

from .models import Universe


class UniverseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'short_description', )
    list_display_links = ('pk', 'name', )
    search_fields = ('name', 'description', )
    list_editable = ()
    list_filter = ()

    fields = ('pk', 'slug', 'name', 'description', 'short_description', )
    readonly_fields = ('pk', )

    save_on_top = True


admin.site.register(Universe, UniverseAdmin)
