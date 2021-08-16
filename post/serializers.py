from rest_framework import serializers
from post.models import Tags, Profile, Categories, Blog

from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class TagsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class ProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('bio', 'birth_date', 'gender', 'location', 'user', 'avatar',)


class BlogSerializers(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = Blog
        fields = ('title', 'content', 'image', 'category', 'tags', 'profile',)


class CreateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    bio = serializers.CharField()
    birth_date = serializers.DateField()
    gender = serializers.CharField()
    location = serializers.CharField(max_length=256, required=False)
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=True)

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise ValidationError("User Name is already taken")
        if User.objects.filter(email__iexact=value).exists():
            raise ValidationError("Email is already taken")
        return value

    def save(self, **kwargs):
        username = self.validated_data['username']
        password = self.validated_data['password']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        bio = self.validated_data['bio']
        birth_date = self.validated_data['birth_date']
        gender = self.validated_data['gender']
        location = self.validated_data['location']

        instance = User.objects.create(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        if password is not None:
            instance.set_password(password)
        instance.save()

        profile = Profile.objects.create(
            user=instance,
            bio=bio,
            birth_date=birth_date,
            gender=gender,
            location=location,
        )

        return profile


