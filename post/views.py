from django.shortcuts import render
from rest_framework.generics import UpdateAPIView, DestroyAPIView, CreateAPIView
from post.serializers import ProfileSerializers, CategorySerializers, BlogSerializers, TagsSerializers


class CategoriesViewCreateUpdate(CreateAPIView):
    queryset = CategorySerializers

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
