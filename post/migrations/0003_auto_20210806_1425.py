# Generated by Django 3.2.4 on 2021-08-06 14:25

from django.db import migrations, models
import post.models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20210806_1321'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='image',
        ),
        migrations.AddField(
            model_name='categories',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=post.models.upload_to_categories),
        ),
    ]
