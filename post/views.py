from oauth2_provider.views import TokenView
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from post.models import Profile, Categories
from post.serializers import ProfileSerializers, CategorySerializers, CreateUserSerializer


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