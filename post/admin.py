from django.contrib import admin
from django.contrib.auth.models import User

from post.models import Tags, Profile, Categories, Blog


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at',)
    list_per_page = 20
    ordering = ('-created_at',)

    fieldsets = [
        ('Details', {'fields': [
            'name', ]})
    ]


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at',)
    list_per_page = 20
    ordering = ('-created_at',)

    fieldsets = [
        ('Details', {'fields': [
            'name', 'image', 'description']})
    ]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at',)
    list_per_page = 20
    ordering = ('-created_at',)
    formfield_querysets = {
        'user': lambda: User.objects.all(),
    }
    fieldsets = [
        ('Details', {'fields': [
            'user', 'bio', 'birth_date', 'gender', 'location', 'avatar', ]})
    ]


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'profile', 'created_at',)
    list_per_page = 20
    ordering = ('-created_at',)
    list_filter = ('category',)
    fieldsets = [
        ('Details', {'fields': [
            'title', 'content', 'image', 'category', 'tags', 'profile', ]})
    ]
