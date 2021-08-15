import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import Group, AbstractUser
from django.contrib.auth.models import User
from django.db import models


def name_path_file(path, filename):
    import uuid
    uuid_for_filename = uuid.uuid4().hex[:6]
    filename = "{uuid}-{filename}".format(
        uuid=uuid_for_filename,
        filename=filename,
    )
    return '/'.join([path, filename])


def upload_to_profile(instance, filename):
    return name_path_file('images/profiles/', filename)

def upload_to_categories(instance, filename):
    return name_path_file('images/categories/', filename)

def upload_to_blog(instance, filename):
    return name_path_file('images/blog/', filename)

def codeGenerator():
    return f'{uuid.uuid4().hex[:4].upper()}'


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tags(BaseModel):
    class Meta:
        verbose_name = "Tags"
        verbose_name_plural = "Tags"

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name}"


class Categories(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to=upload_to_categories, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Profile(BaseModel):
    Gender = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
        ('Rather not to say', 'Rather not to say'),
    )

    bio = models.CharField(max_length=256, null=True, blank=True)
    birth_date = models.DateField(verbose_name='Birthday')
    gender = models.CharField(choices=Gender, max_length=32, default="", verbose_name='Gender')
    location = models.CharField(max_length=256, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    avatar = models.ImageField(upload_to=upload_to_profile, null=True, blank=True)

    def __str__(self):
        return f"{self.user.last_name}, {self.user.first_name}"


class Blog(BaseModel):
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField(max_length=255)
    image = models.ImageField(upload_to=upload_to_blog, null=True, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.title} by {self.profile}'
