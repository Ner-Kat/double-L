from math import ceil
import bleach

from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.template.defaultfilters import slugify
from django.utils.html import strip_tags
from django.template.defaultfilters import truncatechars_html

from users.utils import UserContextMixin

from .models import Post, Category
from .forms import PostAddForm
import posts.settings as settings
import dl_portal.settings as global_settings


class PostsList(UserContextMixin, ListView):
    model = Post
    template_name = 'posts/list.html'
    context_object_name = 'posts'

    def get_category(self):
        if hasattr(self, 'category'):
            return self.category

        category_slug = self.kwargs['category_slug'] if 'category_slug' in self.kwargs else None
        if category_slug is not None:
            self.category = get_object_or_404(Category, slug=category_slug)
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

        title = "Посты в категории {0}".format(str.lower(category.name)) if category is not None else "Список постов"
        context = {
            'title': title,
            'user_category': self.get_category(),
            'login_next': self.request.path_info,
            'pages_num': pages_num,
            'page': page,
            'is_last_page': is_last_page,
            'is_first_page': is_first_page,
            'list_url': reverse_lazy('category', kwargs={'category_slug': category.slug}) if category else reverse_lazy('posts_list'),
            **self.get_user_context(),
            **super().get_context_data(**kwargs),
        }

        if context['posts'] is None:
            raise Http404()

        return context

    def get_queryset(self):
        result = Post.objects.select_related('category', 'author')
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
    pk_url_kwarg = 'post_slug'
    template_name = 'posts/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = {
            'prev_url': self.request.META.get('HTTP_REFERER'),
            'login_next': self.request.path_info,
            **self.get_user_context(),
            **super().get_context_data(**kwargs)
        }
        context_adding = {
            'title': context['post'].title,
            'user_category': context['post'].category,
        }
        return {**context, **context_adding}

    def get_object(self, queryset=None):
        if 'post_id' in self.kwargs:
            return Post.objects.select_related('category', 'author').get(pk=self.kwargs['post_id'])
        if 'post_slug' in self.kwargs:
            return Post.objects.select_related('category', 'author').get(slug=self.kwargs['post_slug'])
        return None


class AddPost(LoginRequiredMixin, UserContextMixin, CreateView):
    template_name = 'posts/add_post.html'
    form_class = PostAddForm

    def get_context(self):
        return {
            'title': 'Добавление поста',
            'login_next': self.request.path_info,
        }

    def get_reflected_context(self, form):
        return {
            'form': form if form else self.form_class,
            **self.get_context()
        }

    def get_context_data(self, **kwargs):
        context = {
            **self.get_context(),
            **self.get_user_context(),
            **super().get_context_data(**kwargs)
        }
        return context

    def post(self, request, *args, **kwargs):
        form = PostAddForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            filtered_content = bleach.clean(post.content, tags=global_settings.ALLOWED_TAGS, strip=True)
            post.short_content = truncatechars_html(filtered_content, 200)
            if not post.slug:
                post.slug = slugify(post.title)
            post.save()

            messages.add_message(request, messages.INFO, 'Материал добавлен!')
            return redirect(post.get_absolute_url())
        else:
            messages.add_message(request, messages.ERROR, 'Материал не был добавлен.')
            return render(request, self.template_name, self.get_reflected_context(form))
