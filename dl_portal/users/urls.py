from django.urls import path
from .views import *

urlpatterns = [
    # path('', UsersList.as_view(), name='users_list'),
    # path('list/', UsersList.as_view(), name='users_list'),
    # path('list/<int:page_id>/', UsersList.as_view(), name='users_list'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('registration/', Registration.as_view(), name='registration'),
    path('<slug:username>/', UserProfile.as_view(), name='userprofile'),
]
