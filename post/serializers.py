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


class ProfileMiniSerializers(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField('get_avatar')
    full_name = serializers.SerializerMethodField('get_full_name')

    def get_full_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        self.request = context.get('request', None)
        super(ProfileMiniSerializers, self).__init__(*args, **kwargs)

    def get_avatar(self, obj: Profile):
        request = self.context.get("request")
        if not request:
            return obj.get_profile_pic
        return request.build_absolute_uri(obj.get_profile_pic)

    class Meta:
        model = Profile
        fields = ('bio', 'birth_date', 'gender', 'location', 'user', 'avatar', 'full_name')


class ProfileSerializers(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField('get_avatar')
    full_name = serializers.SerializerMethodField('get_full_name')

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        self.request = context.get('request', None)
        super(ProfileSerializers, self).__init__(*args, **kwargs)

    def get_full_name(self, obj: Profile):
        return f'{obj.user.first_name}, {obj.user.last_name}'

    def get_avatar(self, obj):
        if not self.request:
            return obj.get_profile_pic
        else:
            return self.request.build_absolute_uri(obj.get_profile_pic)


    class Meta:
        model = Profile
        fields = ('bio', 'birth_date', 'gender', 'location', 'user', 'avatar', 'full_name')


class CategoryMiniSerializers(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('id','name',)


class BlogSerializers(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    profile = ProfileMiniSerializers(read_only=True)
    category = CategoryMiniSerializers(read_only=True)

    class Meta:
        model = Blog
        fields = ('id','title', 'content', 'image', 'category', 'tags', 'profile', 'created_at')


class BlogMiniSerializers(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('id', 'title', 'content', 'image', 'category', 'tags', 'created_at')


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


