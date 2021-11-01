from django.views.generic.base import TemplateView
from django.views import View
from django.http import HttpResponse

from users.utils import UserContextMixin

from posts.models import Post


class Home(UserContextMixin, TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        posts = Post.objects.select_related('category', 'author')[:10]

        context = {
            'title': 'Главная',
            'login_next': self.request.path_info,
            'posts': posts,
            **self.get_user_context(),
            **super().get_context_data()
        }
        return context


class Page(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')
