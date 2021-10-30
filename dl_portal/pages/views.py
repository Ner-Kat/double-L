from django.views.generic.base import TemplateView
from django.views import View
from django.http import HttpResponse

from posts.models import Post


class Home(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        posts = Post.objects.prefetch_related('category')[:10]

        context = {
            'title': 'Главная',
            'posts': posts,
            **super().get_context_data()
        }
        return context


class Page(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')
