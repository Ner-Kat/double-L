from math import ceil

from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from users.utils import UserContextMixin

from .models import Post, Category
from .forms import PostForm
import posts.settings as settings


class PostsList(UserContextMixin, ListView):
    model = Post
    template_name = 'posts/list.html'
    context_object_name = 'posts'

    def get_category(self):
        if hasattr(self, 'category'):
            return self.category

        category_id = self.kwargs['category_id'] if 'category_id' in self.kwargs else None
        if category_id is not None:
            self.category = get_object_or_404(Category, id=category_id)
        else:
            self.category = None

        return self.category

    def get_pages_num(self, category):
        num = Post.objects.aggregate(num=Count('id'))['num']
        if category:
            return ceil(num / settings.PAGE_SIZE_IN_CAT)
        else:
            return ceil(num / settings.PAGE_SIZE)

    def get_page(self):
        if 'page_id' in self.kwargs:
            return self.kwargs['page_id']

        return 1

    def get_context_data(self, *, object_list=None, **kwargs):
        category = self.get_category()
        pages_num = self.get_pages_num(category)
        page = self.get_page()
        is_last_page = page == pages_num
        is_first_page = page == 1

        title = "Посты в категории {0}".format(str.lower(category.title)) if category is not None else "Список постов"
        context = {
            'title': title,
            'user_category': self.get_category(),
            'pages_num': pages_num,
            'page': page,
            'is_last_page': is_last_page,
            'is_first_page': is_first_page,
            'list_url': reverse_lazy('category') if category else reverse_lazy('posts_list'),
            **self.get_user_context(),
            **super().get_context_data(**kwargs),
        }

        if context['posts'] is None:  # or len(context['posts']) == 0:
            raise Http404()

        return context

    def get_queryset(self):
        result = Post.objects.select_related('category')
        page_id = self.get_page()

        category = self.get_category()
        if category is not None:
            result = result.filter(category=category)
            first = (page_id - 1) * settings.PAGE_SIZE_IN_CAT
            last = page_id * settings.PAGE_SIZE_IN_CAT
        else:
            first = (page_id - 1) * settings.PAGE_SIZE
            last = page_id * settings.PAGE_SIZE

        return result.order_by('-created_at')[first:last]


class FullPost(UserContextMixin, DetailView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'posts/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = {
            'prev_url': self.request.META.get('HTTP_REFERER'),
            **self.get_user_context(),
            **super().get_context_data(**kwargs)
        }
        context_adding = {
            'title': context['post'].title,
            'user_category': context['post'].category,
        }
        return {**context, **context_adding}

    def get_object(self, queryset=None):
        return Post.objects.select_related('category').get(pk=self.kwargs['post_id'])


class AddPost(LoginRequiredMixin, UserContextMixin, CreateView):
    template_name = 'posts/add_post.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = {
            'title': 'Добавление поста',
            **self.get_user_context(),
            **super().get_context_data(**kwargs)
        }
        return context
