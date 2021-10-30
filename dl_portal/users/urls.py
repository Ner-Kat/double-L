from django.urls import path
from .views import *

urlpatterns = [
    # path('', UsersList.as_view(), name='users_list'),
    # path('list/', UsersList.as_view(), name='users_list'),
    # path('list/<int:page_id>/', UsersList.as_view(), name='users_list'),
    # path('<str:username>/', UserInfo.as_view(), name='userinfo'),
    path('login/', Login.as_view(), name='login'),
    path('registration/', Registration.as_view(), name='registration'),
]
