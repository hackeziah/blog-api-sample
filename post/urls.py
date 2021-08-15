from django.urls import path

from post.views import CategoriesViewCreateUpdate, ProfileDetailUpdate, CreateUser

urlpatterns = [
    path('api/tags', CategoriesViewCreateUpdate.as_view(), name='tags'),
    path('api/profile/<str:username>', ProfileDetailUpdate.as_view(), name='profile-username'),  # get and update auth
    path('api/register', CreateUser.as_view(), name='register'),
]
