from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('p/<slug:page_slug>/', Page.as_view(), name='page'),
]
