from rest_framework import serializers
from post.models import Tags, Profile, Categories, Blog


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
    class Meta:
        model = Blog
        fields = ('title', 'content', 'image', 'category', 'tags', 'profile',)
