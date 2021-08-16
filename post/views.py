from oauth2_provider.views import TokenView
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from post.models import Profile, Categories, Tags, Blog
from post.serializers import ProfileSerializers, CategorySerializers, CreateUserSerializer, BlogSerializers


class BlogList(ListAPIView):
    serializer_class = BlogSerializers
    queryset = Blog.objects.all()


class CategoriesViewCreateUpdate(ListAPIView):
    serializer_class = CategorySerializers
    queryset = Categories.objects.all()


class ProfileDetailUpdate(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializers
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()

    def get_object(self):
        username = self.kwargs["username"]
        profile = Profile.objects.get(user__username__exact=username)
        return profile

    def get(self, request, *args, **kwargs):
        context = {'request': request}
        username = self.kwargs['username']
        try:
            profile = Profile.objects.get(user__username__exact=username)
        except Profile.DoesNotExist:
            data = {
                'status': False,
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'Profile Not Found!'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializers(profile, context=context)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user = request.user
        username = self.kwargs["username"]
        profile = Profile.objects.get(user__username__exact=username)
        if profile.user == user:
            avatar = request.data.get('avatar', None)
            self.update(request, *args, **kwargs)
            if avatar == 'None':
                profile.avatar = '/static/profiles/default.jpg'
                profile.save()

            if avatar:
                profile.avatar = avatar
                profile.save()
            my_profile = Profile.objects.get(id=profile.pk)
            serializer = self.serializer_class(my_profile)
            return Response(serializer.data)
        data = {
            'status': 'failed',
            'code': status.HTTP_401_UNAUTHORIZED,
            'message': 'Your not authorized to edit this!'
        }
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)


class CreateUser(CreateAPIView, TokenView):
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


class BlogCreate(CreateAPIView, ):
    serializer_class = BlogSerializers
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        category = data.get('category')
        tags = data.get('tags')
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            category = Categories.objects.get(id=category)
        except Tags.DoesNotExist:
            data = {
                'status': False,
                'code': 404,
                "message": "Tags not exist"
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        blog = Blog.objects.create(
            profile=profile,
            title=data.get('title'),
            content=data.get('content'),
            image=data.get('image'),
            category=category,
        )
        if tags is not None:
            for tag_name in tags:
                tag_instance = Tags.objects.filter(name=tag_name).first()
                if not tag_instance:
                    tag_instance = Tags.objects.create(name=tag_name)
                blog.tags.add(tag_instance)
        blog.save()
        serializer = BlogSerializers(blog, many=False)
        data = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            "data": serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)


class BlogUpdateViewDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = BlogSerializers
    permission_classes = (IsAuthenticated,)
    queryset = Blog.objects.all()

    def get_object(self):
        id = self.kwargs["id"]
        blog = Blog.objects.get(id=id)
        return blog

    def get(self, request, *args, **kwargs):
        id = self.kwargs["id"]
        try:
            blog = Blog.objects.get(id=id)
        except Blog.DoesNotExist:
            data = {
                'status': False,
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'Blog Not Found!'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        serializer = BlogSerializers(blog, context={'request': self.request})
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user = request.user
        id = self.kwargs["id"]
        try:
            blog = Blog.objects.get(id=id)
        except Blog.DoesNotExist:
            data = {
                'status': False,
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'Blog Not Found!'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        if blog.profile.user == user:
            self.update(request, *args, **kwargs)
            my_blog = Blog.objects.get(id=blog.pk)
            serializer = BlogSerializers(my_blog, context={'request': self.request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        data = {
            'status': 'failed',
            'code': status.HTTP_401_UNAUTHORIZED,
            'message': 'Your not authorized to edit this!'
        }
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        id = self.kwargs["id"]
        try:
            blog = Blog.objects.get(id=id)
        except Blog.DoesNotExist:
            data = {
                'status': False,
                'code': status.HTTP_404_NOT_FOUND,
                'message': 'Blog Not Found!'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        if blog.profile.user == user:
            self.destroy(request, *args, **kwargs)
            data = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Blog is successfully deleted!'
            }
            return Response(data, status=status.HTTP_200_OK)
        data = {
            'status': 'failed',
            'code': status.HTTP_401_UNAUTHORIZED,
            'message': 'Your not authorized to delete this!'
        }
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)
