from django.contrib import admin

from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'category', 'title', 'created_at', 'author', )
    list_display_links = ('pk', 'title', )
    search_fields = ('title', 'content', )
    list_editable = ('category', 'author', )
    list_filter = ('category', 'author', )

    fields = ('pk', 'slug', 'title', 'category', 'universe', 'author', 'content', 'created_at', 'source', 'views',
              'rating', 'preview_banner')
    readonly_fields = ('pk', 'created_at', 'views', 'rating', )

    save_on_top = True


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'universe', 'name', )
    list_display_links = ('pk', 'name', )
    search_fields = ('name', )
    list_editable = ('universe', )
    list_filter = ('universe', )

    fields = ('pk', 'slug', 'name', 'universe', 'description', 'parent', )
    readonly_fields = ('pk', )

    save_on_top = True


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
