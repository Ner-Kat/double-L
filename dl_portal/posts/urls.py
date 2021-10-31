from django.urls import path
from .views import *

urlpatterns = [
    path('', PostsList.as_view(), name='posts_home'),
    path('add/', AddPost.as_view(), name='add_post'),
    path('list/', PostsList.as_view(), name='posts_list'),
    path('list/<int:page_id>/', PostsList.as_view(), name='posts_list'),
    path('cat/<slug:category_slug>/', PostsList.as_view(), name='category'),
    path('cat/<slug:category_slug>/<int:page_id>/', PostsList.as_view(), name='category'),
    path('<slug:post_slug>/', FullPost.as_view(), name='post'),
]
