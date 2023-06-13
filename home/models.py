from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.name


class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Comment by {self.user}"


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=50)
    desc = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='blog/blog_post_pictures')
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    commented_by = models.ManyToManyField(Comment, related_name='comments')
    liked_by = models.ManyToManyField(User, related_name='likes')
    dateTimepublishedby = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Blog(models.Model):
    title = models.CharField(max_length=100)
    #slug = models.SlugField(max_length=255, unique=True,)
    content = models.TextField()
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title