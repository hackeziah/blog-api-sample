from django.urls import path, include

from post.views import CategoriesViewCreateUpdate

urlpatterns = [
    path('api/tags', CategoriesViewCreateUpdate.as_view(), name='tags'),
]
