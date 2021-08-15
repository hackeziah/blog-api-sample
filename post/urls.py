from django.urls import path, include

from post.views import CategoriesViewCreateUpdate, ProfileDetailUpdate

urlpatterns = [
    path('api/tags', CategoriesViewCreateUpdate.as_view(), name='tags'),
    path('api/profile/<str:username>', ProfileDetailUpdate.as_view(), name='profile-username'),  # get and update auth

]
