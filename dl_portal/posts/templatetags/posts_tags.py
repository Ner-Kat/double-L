from django import template

from posts.models import Category

register = template.Library()


@register.simple_tag(name="get_categories")
def get_categories():
    return Category.objects.order_by('name')


@register.inclusion_tag('posts/tags/list_categories.html')
def show_categories(user_category=None):
    categories = Category.objects.order_by('name')
    return {"categories": categories, "user_category": user_category}
