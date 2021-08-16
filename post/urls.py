from django.urls import path

from post.views import CategoriesViewCreateUpdate, ProfileDetailUpdate, CreateUser, BlogCreate, BlogList, \
    BlogUpdateViewDestroy

urlpatterns = [
    path('api/tags', CategoriesViewCreateUpdate.as_view(), name='tags'),
    path('api/profile/<str:username>', ProfileDetailUpdate.as_view(), name='profile-username'),  # get and update auth
    path('api/register', CreateUser.as_view(), name='register'),
    path('api/blog-create', BlogCreate.as_view(), name='blog-create'),
    path('api/blogs', BlogList.as_view(), name='blogs'),
    path('api/blog/<str:id>', BlogUpdateViewDestroy.as_view(), name='blog'),

]
