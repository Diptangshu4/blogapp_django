# Generated by Django 4.2.2 on 2023-06-13 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_blog_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='slug',
        ),
    ]
